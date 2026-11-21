"""
symptoms_train_examples_test.py

Train an SVM on symptom phrases (labels derived from weights),
test it on example_texts, and produce a confusion matrix.
"""

from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.svm import SVC
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score,
)
import numpy as np
from collections import Counter

PROBLEMS = ["rumination", "procrastination", "self_criticism",
            "burnout", "avoidance"]


# ─────────────────────────────────────────────────────────────
# 1. Load symptoms (training data)
# ─────────────────────────────────────────────────────────────

print("Connecting to MongoDB...")
client = MongoClient("mongodb://localhost:27017")
db = client["psych_support"]

symptoms = list(db.symptoms.find({}))
print(f"Symptoms loaded: {len(symptoms)}")


def symptom_label(sym):
    """Return the problem with the highest weight."""
    weights = sym.get("weights", {})
    if not weights:
        return None
    return max(weights.items(), key=lambda x: x[1])[0]


X_train_text = []
y_train = []
for sym in symptoms:
    label = symptom_label(sym)
    if label is None:
        continue
    X_train_text.append(sym["phrase"])
    y_train.append(label)

print(f"Training examples after filtering: {len(X_train_text)}")
print("Per class:", dict(Counter(y_train)))
print()


# ─────────────────────────────────────────────────────────────
# 2. Load examples (testing data)
# ─────────────────────────────────────────────────────────────

examples = list(db.example_texts.find({}))
X_test_text = [e["text"] for e in examples]
y_test = [e["problem"] for e in examples]

print(f"Test examples: {len(X_test_text)}")
print("Per class:", dict(Counter(y_test)))
print()


# ─────────────────────────────────────────────────────────────
# 3. Encode everything
# ─────────────────────────────────────────────────────────────

print("Loading embedding model...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Encoding symptoms (training data)...")
X_train = embed_model.encode(X_train_text, convert_to_numpy=True,
                             normalize_embeddings=True)

print("Encoding examples (test data)...")
X_test = embed_model.encode(X_test_text, convert_to_numpy=True,
                            normalize_embeddings=True)
print()


# ─────────────────────────────────────────────────────────────
# 4. Train SVM
# ─────────────────────────────────────────────────────────────

print("Training SVM...")
clf = SVC(
    kernel="rbf",
    C=5.0,
    gamma="scale",
    class_weight="balanced",
    probability=True,
)
clf.fit(X_train, y_train)
print("Training complete.\n")


# ─────────────────────────────────────────────────────────────
# 5. Predict on test examples
# ─────────────────────────────────────────────────────────────

y_pred = clf.predict(X_test)


# ─────────────────────────────────────────────────────────────
# 6. Confusion matrix
# ─────────────────────────────────────────────────────────────

labels = sorted(set(y_test) | set(y_pred))
cm = confusion_matrix(y_test, y_pred, labels=labels)

print("=" * 90)
print("CONFUSION MATRIX (rows = actual example, columns = predicted)")
print("=" * 90)
header = "actual \\ pred".ljust(18)
for lbl in labels:
    header += lbl[:10].rjust(12)
print(header)
print("-" * 90)

for i, actual in enumerate(labels):
    row = actual.ljust(18)
    for j, pred in enumerate(labels):
        count = cm[i][j]
        marker = " *" if i == j and count > 0 else ""
        row += f"{count:>10}{marker}  "
    print(row)
print("-" * 90)


# ─────────────────────────────────────────────────────────────
# 7. Per-class metrics
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 90)
print("PER-CLASS METRICS")
print("=" * 90)
print(classification_report(y_test, y_pred, labels=labels, zero_division=0))


# ─────────────────────────────────────────────────────────────
# 8. Overall accuracy
# ─────────────────────────────────────────────────────────────

acc = accuracy_score(y_test, y_pred)
print("=" * 90)
print(f"OVERALL ACCURACY: {acc:.3f} ({int(acc * len(y_test))}/{len(y_test)})")
print("=" * 90)


# ─────────────────────────────────────────────────────────────
# 9. Misclassifications
# ─────────────────────────────────────────────────────────────

print("\n" + "=" * 90)
print("MISCLASSIFICATIONS")
print("=" * 90)

misclassified = [(X_test_text[i], y_test[i], y_pred[i])
                 for i in range(len(y_test)) if y_test[i] != y_pred[i]]

if not misclassified:
    print("None.")
else:
    for text, actual, predicted in misclassified[:30]:
        preview = text[:120] + ("..." if len(text) > 120 else "")
        print(f"  actual: {actual:18s}  predicted: {predicted:18s}")
        print(f"    {preview}")
        print()

print(f"Total misclassifications: {len(misclassified)}/{len(y_test)}")