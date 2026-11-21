"""
interactive_predictor.py — ROUTED predictor.

Routing rule:
  1. Check if the input contains a negation near any matched symptom.
  2. If YES → rules decide (SVM is NOT consulted).
  3. If NO  → SVM decides.
"""

from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.svm import SVC
import numpy as np
from collections import Counter

import hybrid_matcher as hm

PROBLEMS = ["rumination", "procrastination", "self_criticism",
            "burnout", "avoidance"]


# ─────────────────────────────────────────────────────────────
# 1. Load symptoms and train SVM
# ─────────────────────────────────────────────────────────────

print("Connecting to MongoDB...")
client = MongoClient("mongodb://localhost:27017")
db = client["psych_support"]

symptoms = list(db.symptoms.find({}))
print(f"Symptoms loaded: {len(symptoms)}")


def symptom_label(sym):
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

print(f"Training phrases: {len(X_train_text)}")
print("Per class:", dict(Counter(y_train)))
print()

print("Loading embedding model...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

print("Encoding symptoms...")
X_train = embed_model.encode(X_train_text, convert_to_numpy=True,
                             normalize_embeddings=True)

print("Training SVM...")
clf = SVC(
    kernel="rbf",
    C=5.0,
    gamma="scale",
    class_weight="balanced",
    probability=True,
)
clf.fit(X_train, y_train)
print("SVM trained.\n")


# ─────────────────────────────────────────────────────────────
# 2. SVM prediction
# ─────────────────────────────────────────────────────────────

def svm_predict(text):
    vec = embed_model.encode([text], convert_to_numpy=True,
                             normalize_embeddings=True)
    probs = clf.predict_proba(vec)[0]
    return {cls: float(p) for cls, p in zip(clf.classes_, probs)}


# ─────────────────────────────────────────────────────────────
# 3. Negation check via rules
# ─────────────────────────────────────────────────────────────

def has_negation(text):
    """
    Returns (has_negation, matches, tier).
    has_negation = True if any matched symptom is affected by negation.
    """
    matches, tier = hm.find_matches(text)

    for entry, form, suppressed in matches:
        if suppressed:
            return True, matches, tier
        if any(w in hm.NEGATION_WORDS for w in form.split()):
            return True, matches, tier

    return False, matches, tier


# ─────────────────────────────────────────────────────────────
# 4. Routed analyze
# ─────────────────────────────────────────────────────────────

def analyze(text):
    print("=" * 70)
    print("INPUT:", text)
    print("-" * 70)

    has_neg, matches, tier = has_negation(text)

    if has_neg:
        # Route 1: negation detected → rules decide
        print(f"[ROUTE] NEGATION detected (tier {tier}) → rules decide")
        print("        (SVM bypassed — it does not handle negation)")
        for entry, form, suppressed in matches:
            flag = " [SUPPRESSED]" if suppressed else ""
            print(f"   [{entry['_id']}]  {entry['phrase']}  ('{form}'){flag}")

        live = [m for m in matches if not m[2]]
        if live:
            scores = hm.rule_scores(matches)
            final_probs = hm.softmax(scores, temperature=0.3)
            method = "rules (negation present, live signal)"
        else:
            final_probs = {p: 1.0 / len(PROBLEMS) for p in PROBLEMS}
            method = "rules → uniform (all matches suppressed)"

    else:
        # Route 2: no negation → SVM decides
        print("[ROUTE] NO NEGATION detected → SVM decides")
        if matches:
            for entry, form, suppressed in matches:
                print(f"   [{entry['_id']}]  {entry['phrase']}  ('{form}')")
        else:
            print("   (rules found no matching symptoms)")

        final_probs = svm_predict(text)
        method = "SVM (embeddings + trained model)"

    # Rank and display
    print(f"[METHOD] {method}")
    print("-" * 70)

    ranked = sorted(final_probs.items(), key=lambda x: x[1], reverse=True)
    for problem, prob in ranked:
        bar = "█" * int(prob * 40)
        print(f"  {problem:18s} {prob*100:5.1f}%  {bar}")

    print("=" * 70 + "\n")
    return ranked


# ─────────────────────────────────────────────────────────────
# 5. Interactive loop
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Routed predictor ready. Type a sentence ('quit' to exit).\n")
    while True:
        try:
            text = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break
        if not text:
            continue
        if text.lower() in {"quit", "exit", "q"}:
            print("Bye.")
            break
        analyze(text)