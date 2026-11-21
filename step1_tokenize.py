"""
step1_tokenize.py — Step 1 of the matcher pipeline.

Goal: take user text, lowercase it, tokenize it, and lemmatize each token.
This is the foundation — no matching, no scoring, just clean tokens.
"""

import spacy

# Load the small English model (must be installed via:
#   pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz)
nlp = spacy.load("en_core_web_sm")


def process(text: str):
    """
    Lowercase, tokenize, and lemmatize a piece of user text.

    - Lowercase: 'I Can't Sleep' → "i can't sleep"
    - Tokenize: splits into words and punctuation
    - Remove punctuation and whitespace tokens
    - Lemmatize: 'replaying' → 'replay', 'thoughts' → 'thought'

    Returns a list of lemmatized tokens.
    """
    text = text.lower()
    doc = nlp(text)
    tokens = [
        t.lemma_
        for t in doc
        if not t.is_punct and not t.is_space
    ]
    return tokens


if __name__ == "__main__":
    # A realistic example — mixture of rumination + burnout signals
    sentence = (
        "Lately I can't sleep and I keep replaying that conversation "
        "in my head. I'm so tired."
    )

    result = process(sentence)

    print("Original text:")
    print(sentence)
    print()
    print("Raw tokens (lemmatized):")
    print(result)
    print()
    print("Token count:", len(result))