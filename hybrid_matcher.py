"""
hybrid_matcher.py — four-tier matcher.

Tier 1: phrase contains negation → keep
Tier 2: modal + not → strip, re-match affirmation, keep original
Tier 2b: be/do + not → suppress
Tier 3: no negation, match found → keep
Tier 4: no matches anywhere → fall back to embeddings
Tier 5: still nothing → uniform 20% across all 5
"""

import spacy
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np
from collections import defaultdict

# ─────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────

PROBLEMS = ["rumination", "procrastination", "self_criticism",
            "burnout", "avoidance"]

NEGATION_WORDS = {"not", "no", "never", "none",
                  "nobody", "nothing", "nowhere",
                  "neither", "nor"}

MODAL_AUX = {"can", "could", "will", "would", "should",
             "may", "might", "must", "shall"}

BE_AUX = {"be", "am", "is", "are", "was", "were", "being", "been"}

DO_AUX = {"do", "does", "did"}

THRESHOLD = 0.45
TEMPERATURE = 0.05

# ─────────────────────────────────────────────────────────────
# Load everything once
# ─────────────────────────────────────────────────────────────

print("Loading spaCy...")
nlp = spacy.load("en_core_web_sm")

print("Connecting to MongoDB...")
client = MongoClient("mongodb://localhost:27017")
db = client["psych_support"]

print("Loading symptoms and examples...")
SYMPTOMS = list(db.symptoms.find({}))
EXAMPLES = list(db.example_texts.find({}))
print(f"  Symptoms: {len(SYMPTOMS)}")
print(f"  Examples: {len(EXAMPLES)}\n")

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded.\n")

# ─────────────────────────────────────────────────────────────
# Text processing
# ─────────────────────────────────────────────────────────────

def process(text: str):
    text = text.lower()
    doc = nlp(text)
    return [t.lemma_ for t in doc if not t.is_punct and not t.is_space]


def generate_ngrams(tokens, max_n=8):
    ngrams = set()
    for n in range(1, max_n + 1):
        for i in range(len(tokens) - n + 1):
            ngrams.add(" ".join(tokens[i:i + n]))
    return ngrams


def build_lexicon_index():
    index = []
    for sym in SYMPTOMS:
        forms = [sym["phrase"]] + sym.get("variants", [])
        normalized = []
        for f in forms:
            tokens = process(f)
            if tokens:
                normalized.append(" ".join(tokens))
        index.append({
            "_id": sym["_id"],
            "phrase": sym["phrase"],
            "forms": normalized,
            "weights": sym.get("weights", {}),
        })
    return index


LEXICON = build_lexicon_index()

# ─────────────────────────────────────────────────────────────
# Gap-aware phrase matching
# ─────────────────────────────────────────────────────────────

def phrase_matches_with_gaps(tokens, form_tokens, max_gap=2):
    """
    Return the (start, end) index span where the phrase matches,
    allowing up to `max_gap` filler tokens between consecutive
    form tokens. Returns (-1, -1) if no match.
    """
    n = len(tokens)
    m = len(form_tokens)
    if m == 0 or m > n:
        return (-1, -1)

    for start in range(n - m + 1):
        i = start
        j = 0
        gaps_used = 0
        last_match_index = start
        while j < m and i < n:
            if tokens[i] == form_tokens[j]:
                last_match_index = i
                i += 1
                j += 1
                gaps_used = 0
            else:
                gaps_used += 1
                if gaps_used > max_gap:
                    break
                i += 1
        if j == m:
            return (start, last_match_index + 1)
    return (-1, -1)


# ─────────────────────────────────────────────────────────────
# Negation classification
# ─────────────────────────────────────────────────────────────

def classify_negation_at(tokens, start, end, window=6):
    """
    Simplified negation classification.

    1. If there is NO negation word near the match → "none".
    2. If there IS a negation word:
       a. If the negation is INSIDE the matched span (baked-in) → "baked".
       b. If the token before the negation is be/do → "predicate".
       c. If the token before the negation is a modal → "modal".
    """
    span = tokens[start:end]

    # Check for negation inside the span
    for i, w in enumerate(span):
        if w in NEGATION_WORDS:
            # Look at up to 2 tokens before the negation
            zone = (span[max(0, i - 2):i] if i >= 1
                    else tokens[max(0, start - 2):start])
            for aux in reversed(zone):
                if aux in BE_AUX or aux in DO_AUX:
                    return "predicate"
                if aux in MODAL_AUX:
                    return "modal"
            return "predicate"

    # Check for negation in the window before the match
    before = tokens[max(0, start - window):start]
    for j in range(len(before) - 1, -1, -1):
        if before[j] in NEGATION_WORDS:
            zone = before[max(0, j - 2):j]
            for aux in reversed(zone):
                if aux in BE_AUX or aux in DO_AUX:
                    return "predicate"
                if aux in MODAL_AUX:
                    return "modal"
            return "predicate"

    return "none"

def strip_negation_from_tokens(tokens):
    """Remove negation words from a token list."""
    return [t for t in tokens if t not in NEGATION_WORDS]


# ─────────────────────────────────────────────────────────────
# Main rule matcher — Tiers 1-3
# ─────────────────────────────────────────────────────────────

def find_matches(user_text):
    """
    Returns (matches, tier)
      matches: list of (entry, form, suppressed: bool)
      tier:    string describing which tiers fired
    """
    tokens = process(user_text)
    matches = []
    tiers_used = set()

    for entry in LEXICON:
        for form in entry["forms"]:
            form_tokens = form.split()
            start, end = phrase_matches_with_gaps(tokens, form_tokens, max_gap=2)
            if start == -1:
                continue

            verdict = classify_negation_at(tokens, start, end)

            if verdict == "predicate":
                matches.append((entry, form, True))
                tiers_used.add("2b")
            elif verdict == "modal":
                matches.append((entry, form, False))
                tiers_used.add("2")
            elif verdict == "baked":
                matches.append((entry, form, False))
                tiers_used.add("1")
            else:
                matches.append((entry, form, False))
                tiers_used.add("3")
            break

    # Tier 2 extra: re-match the affirmation (negation stripped)
    if "2" in tiers_used:
        stripped = strip_negation_from_tokens(tokens)
        for entry in LEXICON:
            for form in entry["forms"]:
                if any(e["_id"] == entry["_id"] for e, _, _ in matches):
                    continue
                start, end = phrase_matches_with_gaps(
                    stripped, form.split(), max_gap=2)
                if start != -1:
                    matches.append((entry, form, False))
                    break

    tier = "+".join(sorted(tiers_used)) if tiers_used else "none"
    return matches, tier


def rule_scores(matches):
    raw = {p: 0.0 for p in PROBLEMS}
    for entry, form, suppressed in matches:
        if suppressed:
            continue
        for p, w in entry["weights"].items():
            if p in raw:
                raw[p] += w
    return raw


# ─────────────────────────────────────────────────────────────
# Tier 4 — embeddings
# ─────────────────────────────────────────────────────────────

by_problem = defaultdict(list)
for ex in EXAMPLES:
    by_problem[ex["problem"]].append(ex["text"])

centroids = {}
for problem, texts in by_problem.items():
    vectors = model.encode(texts, convert_to_numpy=True,
                           normalize_embeddings=True)
    centroid = vectors.mean(axis=0)
    centroid = centroid / np.linalg.norm(centroid)
    centroids[problem] = centroid


def embedding_scores(user_text):
    vec = model.encode([user_text], convert_to_numpy=True,
                       normalize_embeddings=True)[0]
    sims = {p: float(np.dot(vec, c)) for p, c in centroids.items()}
    return sims


# ─────────────────────────────────────────────────────────────
# Softmax
# ─────────────────────────────────────────────────────────────

def softmax(scores, temperature=TEMPERATURE):
    import math
    vals = {k: max(v, 0.0) for k, v in scores.items()}
    mx = max(vals.values()) if vals else 0
    if mx == 0:
        return {k: 1 / len(vals) for k in vals}
    exp = {k: math.exp((v - mx) / temperature) for k, v in vals.items()}
    total = sum(exp.values())
    return {k: v / total for k, v in exp.items()}


# ─────────────────────────────────────────────────────────────
# Analyze
# ─────────────────────────────────────────────────────────────

def analyze(user_text):
    print("=" * 70)
    print("INPUT:", user_text)
    print("-" * 70)

    matches, tier = find_matches(user_text)
    live = [m for m in matches if not m[2]]

    if live:
        print(f"[RULES] Tier {tier} matched {len(matches)} symptom(s):")
        for entry, form, suppressed in matches:
            flag = "  [SUPPRESSED]" if suppressed else ""
            print(f"   [{entry['_id']}]  {entry['phrase']}  ('{form}'){flag}")
        scores = rule_scores(matches)
        probs = softmax(scores, temperature=0.3)
        used = f"rules (tier {tier})"

    elif matches:
        print(f"[RULES] Tier {tier} — all matches suppressed (predicate negation).")
        probs = {p: 1.0 / len(PROBLEMS) for p in PROBLEMS}
        used = "suppressed → uniform"

    else:
        print("[RULES] No symptoms matched → Tier 4: embeddings")
        scores = embedding_scores(user_text)
        probs = softmax(scores, temperature=0.3)
        used = "embeddings (tier 4)"

    print("-" * 70)

    ranked = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    top_problem, top_prob = ranked[0]

    is_uniform = all(abs(v - 1.0 / len(PROBLEMS)) < 1e-6 for v in probs.values())

    if is_uniform:
        print("⚠  No signal. Uniform 20% across all 5 problems.")
    elif top_prob < THRESHOLD:
        print(f"⚠  No strong match ({used}). Top: {top_problem} "
              f"({top_prob*100:.1f}%).")
        print("   This may not be one of the 5 problems the system recognizes.")
    else:
        print(f"Probabilities ({used}):")
        for p, prob in ranked:
            bar = "█" * int(prob * 40)
            print(f"  {p:18s} {prob*100:5.1f}%  {bar}")

    print("=" * 70 + "\n")
    return ranked


# ─────────────────────────────────────────────────────────────
# Interactive loop
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Four-tier hybrid matcher ready. Type a sentence ('quit' to exit).\n")
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