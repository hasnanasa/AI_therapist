"""
embedding_matcher.py — ML-based matcher using sentence embeddings.

Instead of matching exact phrases, this uses a pretrained sentence
transformer to convert each example into a vector, computes a centroid
per problem, and classifies new text by cosine similarity.
"""

from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np

# ─────────────────────────────────────────────────────────────
# 1. Load the pretrained model
# ─────────────────────────────────────────────────────────────

print("Loading model... (first run downloads ~80MB)")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded.\n")


# ─────────────────────────────────────────────────────────────
# 2. Load examples from MongoDB
# ─────────────────────────────────────────────────────────────

client = MongoClient("mongodb://localhost:27017")
db = client["psych_support"]

examples = list(db.example_texts.find({}))
print(f"Loaded {len(examples)} example texts from MongoDB.\n")


# ─────────────────────────────────────────────────────────────
# 3. Group by problem and compute centroids
# ─────────────────────────────────────────────────────────────

from collections import defaultdict

by_problem = defaultdict(list)
for ex in examples:
    by_problem[ex["problem"]].append(ex["text"])

print("Examples per problem:")
for problem, texts in by_problem.items():
    print(f"  {problem}: {len(texts)}")


# Encode every example, group into per-problem matrices
print("\nEncoding examples... (this takes a few seconds)")
centroids = {}
for problem, texts in by_problem.items():
    vectors = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    centroid = vectors.mean(axis=0)
    # Normalize the centroid
    centroid = centroid / np.linalg.norm(centroid)
    centroids[problem] = centroid

print("Centroids computed.\n")


# ─────────────────────────────────────────────────────────────
# 4. Classify a new sentence
# ─────────────────────────────────────────────────────────────

def classify(user_text: str, temperature: float = 0.05):
    # Encode the user's sentence
    vec = model.encode([user_text], convert_to_numpy=True, normalize_embeddings=True)[0]

    # Cosine similarity to each centroid (vectors already normalized → dot product)
    sims = {p: float(np.dot(vec, c)) for p, c in centroids.items()}

    # Convert to a probability distribution (softmax over similarities)
    vals = np.array(list(sims.values()))
    # Scale similarities to make softmax meaningful
    scaled = (vals - vals.max()) / temperature
    exp = np.exp(scaled)
    probs = exp / exp.sum()

    ranked = sorted(zip(sims.keys(), probs), key=lambda x: x[1], reverse=True)
    return ranked, sims


def analyze(user_text: str):
    ranked, sims = classify(user_text)

    print("=" * 70)
    print("INPUT:", user_text)
    print("-" * 70)
    print("Raw similarities:")
    for p, s in sorted(sims.items(), key=lambda x: x[1], reverse=True):
        print(f"   {p:18s} {s:+.4f}")
    print("-" * 70)

    # ─── Confidence threshold ───
    top_problem, top_prob = ranked[0]
    THRESHOLD = 0.45

    if top_prob < THRESHOLD:
        print(f"⚠  No strong match. Top candidate: {top_problem} "
              f"({top_prob*100:.1f}%) — below confidence threshold "
              f"({THRESHOLD*100:.0f}%).")
        print("   This may not be one of the 5 problems the system recognizes.")
    else:
        print("Probabilities:")
        for p, prob in ranked:
            bar = "█" * int(prob * 40)
            print(f"  {p:18s} {prob*100:5.1f}%  {bar}")

    print("=" * 70 + "\n")
    return ranked

# ─────────────────────────────────────────────────────────────
# 5. Interactive loop
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Type a sentence describing how you feel.")
    print("Type 'quit' to exit.\n")

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