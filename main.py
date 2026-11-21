"""
main.py — the interactive entry point of the matcher.

Run this, type your problem in plain text, and get ranked
probabilities for each of the five problems.
"""

import spacy
from pymongo import MongoClient

# ─────────────────────────────────────────────────────────────
# Setup
# ─────────────────────────────────────────────────────────────

nlp = spacy.load("en_core_web_sm")

NEGATION_WORDS = {"not", "no", "never", "none",
                  "nobody", "nothing", "nowhere",
                  "neither", "nor"}

PROBLEMS = ["rumination", "procrastination", "self_criticism",
            "burnout", "avoidance"]


# ─────────────────────────────────────────────────────────────
# Text processing (Step 1 + 2)
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


# ─────────────────────────────────────────────────────────────
# Load symptoms and build lexicon index (Step 3)
# ─────────────────────────────────────────────────────────────

client = MongoClient("mongodb://localhost:27017")
db = client["psych_support"]
SYMPTOMS = list(db.symptoms.find({}))
print(f"Loaded {len(SYMPTOMS)} symptoms from MongoDB.\n")


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
print(f"Lexicon index built: {len(LEXICON)} entries.\n")


# ─────────────────────────────────────────────────────────────
# Negation (Step 4)
# ─────────────────────────────────────────────────────────────

def phrase_contains_negation(form: str) -> bool:
    return any(w in NEGATION_WORDS for w in form.split())


def is_negated_in_context(tokens, form: str, window: int = 3) -> bool:
    phrase_tokens = form.split()
    plen = len(phrase_tokens)
    for i in range(len(tokens) - plen + 1):
        if tokens[i:i + plen] == phrase_tokens:
            start = max(0, i - window)
            if any(w in NEGATION_WORDS for w in tokens[start:i]):
                return True
    return False


# ─────────────────────────────────────────────────────────────
# Match (Step 3 + 4 combined)
# ─────────────────────────────────────────────────────────────

def find_matches(user_text):
    tokens = process(user_text)
    user_ngrams = generate_ngrams(tokens, max_n=8)
    matches = []
    for entry in LEXICON:
        for form in entry["forms"]:
            if form in user_ngrams:
                if phrase_contains_negation(form):
                    matches.append((entry, form, False))
                    break
                if is_negated_in_context(tokens, form):
                    matches.append((entry, form, True))
                    break
                matches.append((entry, form, False))
                break
    return matches


# ─────────────────────────────────────────────────────────────
# Score (Step 5)
# ─────────────────────────────────────────────────────────────

def score_problems(matches):
    raw = {p: 0.0 for p in PROBLEMS}
    max_possible = {p: 0.0 for p in PROBLEMS}

    for sym in SYMPTOMS:
        for p, w in sym.get("weights", {}).items():
            if p in max_possible:
                max_possible[p] += w

    for entry, form, negated in matches:
        if negated:
            continue
        for p, w in entry["weights"].items():
            if p in raw:
                raw[p] += w

    return {p: (raw[p] / max_possible[p] if max_possible[p] else 0.0)
            for p in PROBLEMS}


def softmax(scores, temperature=0.05):
    """
    Convert raw scores into a probability distribution (sums to 1).
    Temperature controls sharpness — lower = more confident.
    """
    import math
    if not scores:
        return {}
    # Use only positive scores
    vals = {k: max(v, 0.0) for k, v in scores.items()}
    mx = max(vals.values())
    if mx == 0:
        return {k: 1/len(vals) for k in vals}
    exp = {k: math.exp((v - mx) / temperature) for k, v in vals.items()}
    total = sum(exp.values())
    return {k: v / total for k, v in exp.items()}


# ─────────────────────────────────────────────────────────────
# The interactive loop
# ─────────────────────────────────────────────────────────────

def analyze(user_text):
    matches = find_matches(user_text)
    scores = score_problems(matches)
    probs = softmax(scores, temperature=0.05)

    print("\n" + "=" * 70)
    print("INPUT:", user_text)
    print("-" * 70)

    # Matched symptoms
    if matches:
        print(f"Matched {len(matches)} symptom(s):")
        for entry, form, negated in matches:
            flag = "  [NEGATED]" if negated else ""
            print(f"   [{entry['_id']}]  {entry['phrase']}  ('{form}'){flag}")
    else:
        print("No symptoms matched.")
    print("-" * 70)

    # Ranked probabilities
    ranked = sorted(probs.items(), key=lambda x: x[1], reverse=True)

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