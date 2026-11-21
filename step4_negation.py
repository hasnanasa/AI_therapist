"""
step4_negation.py — Step 4 of the matcher pipeline.

Adds negation detection to the matcher from Step 3.
A match is suppressed only when a negation word modifies it
AND the symptom phrase itself does not contain a negation word.
"""

import spacy
from pymongo import MongoClient

nlp = spacy.load("en_core_web_sm")

NEGATION_WORDS = {"not", "no", "never", "none", "nobody", "nothing", "nowhere", "neither", "nor"}


# ─────────────────────────────────────────────────────────────
# Reuse Step 1 & 2
# ─────────────────────────────────────────────────────────────

def process(text: str):
    text = text.lower()
    doc = nlp(text)
    return [t.lemma_ for t in doc if not t.is_punct and not t.is_space]


def generate_ngrams(tokens, max_n=4):
    ngrams = set()
    for n in range(1, max_n + 1):
        for i in range(len(tokens) - n + 1):
            ngrams.add(" ".join(tokens[i:i + n]))
    return ngrams


# ─────────────────────────────────────────────────────────────
# Load symptoms + build lexicon index (same as Step 3)
# ─────────────────────────────────────────────────────────────

client = MongoClient("mongodb://localhost:27017")
db = client["psych_support"]
SYMPTOMS = list(db.symptoms.find({}))
print(f"Loaded {len(SYMPTOMS)} symptoms.\n")


def build_lexicon_index():
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
# Negation detection
# ─────────────────────────────────────────────────────────────

def phrase_contains_negation(form: str) -> bool:
    """Check if the symptom form itself already contains a negation word."""
    return any(word in NEGATION_WORDS for word in form.split())


def is_negated_in_context(tokens, form: str, window: int = 3) -> bool:
    """
    Check whether a negation word appears in the `window` tokens
    immediately before the matched phrase in the user's token stream.

    tokens: the user's token list (lemmatized)
    form:   the normalized symptom form, e.g. "replay"
    window: how many tokens back to look
    """
    phrase_tokens = form.split()
    phrase_len = len(phrase_tokens)

    for i in range(len(tokens) - phrase_len + 1):
        if tokens[i:i + phrase_len] == phrase_tokens:
            start = max(0, i - window)
            preceding = tokens[start:i]
            if any(w in NEGATION_WORDS for w in preceding):
                return True
    return False


# ─────────────────────────────────────────────────────────────
# Match with negation awareness
# ─────────────────────────────────────────────────────────────

def find_matches(user_text: str):
    tokens = process(user_text)
    user_ngrams = generate_ngrams(tokens, max_n=4)

    matches = []
    for entry in LEXICON:
        for form in entry["forms"]:
            if form in user_ngrams:
                # Rule 1: if the phrase itself contains a negation, never suppress
                if phrase_contains_negation(form):
                    matches.append((entry, form, False))
                    break

                # Rule 2: otherwise, check context for negation
                if entry["negation_sensitive"] and is_negated_in_context(tokens, form):
                    matches.append((entry, form, True))
                    break

                matches.append((entry, form, False))
                break
    return matches


# ─────────────────────────────────────────────────────────────
# Run tests
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_sentences = [
        "I keep replaying that conversation in my head.",
        "I don't replay things, I'm fine.",
        "I can't stop thinking about it.",
        "I'm not tired at all.",
        "I am not exhausted, I just have a lot to do.",
        "I'm so exhausted I can't keep going.",
    ]

    for sentence in test_sentences:
        print("=" * 70)
        print("INPUT:", sentence)
        print("-" * 70)
        matches = find_matches(sentence)
        if not matches:
            print("  (no matches)")
        for entry, form, negated in matches:
            flag = " [NEGATED]" if negated else ""
            print(f"  [{entry['_id']}]  {entry['phrase']}  (matched: '{form}'){flag}")
        print()