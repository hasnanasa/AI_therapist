"""
evaluate.py — compute precision, recall, F1, and accuracy
for the hybrid matcher on the labeled test set.
"""

from test_set import TEST_SET
from collections import defaultdict

# ─── Import the analyze() from hybrid_matcher WITHOUT running the loop ───
# Since hybrid_matcher runs an interactive loop on import,
# we re-implement the classification directly here.

import spacy
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np

PROBLEMS = ["rumination", "procrastination", "self_criticism",
            "burnout", "avoidance"]

print("Loading...")
nlp = spacy.load("en_core_web_sm")
client = MongoClient("mongodb://localhost:27017")
db = client["psych_support"]

# Import all the matching logic from hybrid_matcher
import hybrid_matcher as hm


# ─── Run the test set ───

predictions = []  # (expected, predicted_top1, probs)

for text, expected in TEST_SET:
    ranked = hm.analyze(text)
    top_problem = ranked[0][0]
    top_prob = ranked[0][1]

    # If the top probability is below threshold, treat as "none"
    if top_prob < hm.THRESHOLD:
        predicted = "none"
    else:
        predicted = top_problem

    predictions.append((expected, predicted, dict(ranked)))


# ─── Compute per-class metrics ───

classes = PROBLEMS + ["none"]

# Confusion matrix
confusion = {actual: {pred: 0 for pred in classes} for actual in classes}
for expected, predicted, _ in predictions:
    confusion[expected][predicted] += 1

# Per-class precision, recall, F1
print("\n" + "=" * 70)
print(f"{'class':18s} {'precision':>10s} {'recall':>10s} {'f1':>10s} {'support':>10s}")
print("-" * 70)

total_correct = 0
total = len(predictions)

for cls in PROBLEMS:
    tp = confusion[cls][cls]
    fp = sum(confusion[other][cls] for other in classes if other != cls)
    fn = sum(confusion[cls][other] for other in classes if other != cls)
    support = tp + fn

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    total_correct += tp
    print(f"{cls:18s} {precision:>10.3f} {recall:>10.3f} {f1:>10.3f} {support:>10d}")

print("-" * 70)
print(f"{'OVERALL ACCURACY':18s} {total_correct}/{total} = {total_correct/total*100:.1f}%")
print("=" * 70)

# ─── Show misclassifications ───

print("\nMisclassifications:")
print("-" * 70)
for text, expected, (expected_pred_pair) in zip(
    [t for t, _ in TEST_SET], [e for _, e in TEST_SET], predictions
):
    expected, predicted, _ = expected_pred_pair
    if expected != predicted:
        print(f"  expected: {expected:18s}  got: {predicted:18s}")
        print(f"    '{text}'")