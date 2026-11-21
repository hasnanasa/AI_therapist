"""
step3_match.py — Step 3 of the matcher pipeline.

Goal: load symptoms from MongoDB, process each phrase/variant
through the same tokenizer+lemmatizer as the user's text, and
find which symptoms appear in the user's n-grams.

No scoring yet. Just: which symptoms matched, and where.
"""

import spacy
from pymongo import MongoClient

nlp = spacy.load("en_core_web_sm")


# ─────────────────────────────────────────────────────────────
# Reuse Step 1 & 2 functions
# ─────────────────────────────────────────────────────────────

def process(text: str):
    """Lowercase, tokenize, lemmatize."""
    text = text.lower()
    doc = nlp(text)
    return [t.lemma_ for t in doc if not t.is_punct and not t.is_space]


def generate_ngrams(tokens, max_n=4):
    """All contiguous n-grams from length 1 to max_n, as strings."""
    ngrams = set()
    for n in range(1, max_n + 1):
        for i in range(len(tokens) - n + 1):
            ngrams.add(" ".join(tokens[i:i + n]))
    return ngrams


# ─────────────────────────────────────────────────────────────
# Load symptoms from MongoDB
# ─────────────────────────────────────────────────────────────

client = MongoClient("mongodb://localhost:27017")
db = client["psych_support"]
SYMPTOMS = list(db.symptoms.find({}))
print(f"Loaded {len(SYMPTOMS)} symptoms.\n")


# ─────────────────────────────────────────────────────────────
# Pre-process every symptom's phrase + variants into
# normalized strings. Do this ONCE, not per user query.
# ─────────────────────────────────────────────────────────────

def build_lexicon_index():
    """
    For each symptom, produce a list of normalized string forms.
    Example:
      symptom rum_001 has phrase "can't stop thinking"
      → normalized form: "can not stop think"
    """
    index = []
    for sym in SYMPTOMS:
        forms = [sym["phrase"]] + sym.get("variants", [])
        normalized_forms = []
        for f in forms:
            tokens = process(f)
            if tokens:
                normalized_forms.append(" ".join(tokens))
        index.append({
            "_id": sym["_id"],
            "phrase": sym["phrase"],
            "forms": normalized_forms,
            "weights": sym.get("weights", {}),
            "negation_sensitive": sym.get("negation_sensitive", False),
        })
    return index


LEXICON = build_lexicon_index()
print(f"Built lexicon index with {len(LEXICON)} entries.\n")


# ─────────────────────────────────────────────────────────────
# Match user text against lexicon
# ─────────────────────────────────────────────────────────────

def find_matches(user_text: str):
    tokens = process(user_text)
    user_ngrams = generate_ngrams(tokens, max_n=4)

    matches = []
    for entry in LEXICON:
        for form in entry["forms"]:
            if form in user_ngrams:
                matches.append((entry, form))
                break  # one match per symptom is enough
    return matches


# ─────────────────────────────────────────────────────────────
# Run on a test sentence
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sentence = (
        "Lately I can't sleep and I keep replaying that conversation "
        "in my head. I'm so tired."
    )

    print("INPUT:", sentence)
    print()

    matches = find_matches(sentence)

    print(f"Matched {len(matches)} symptoms:\n")
    for entry, form in matches:
        print(f"  [{entry['_id']}]  {entry['phrase']}")
        print(f"        matched form: '{form}'")
        print(f"        weights: {entry['weights']}")
        print()