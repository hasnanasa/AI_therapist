"""
step2_ngrams.py — Step 2 of the matcher pipeline.

Goal: take the tokens from Step 1 and generate all contiguous
n-gram sequences from 1 to max_n words. This is what lets us
match multi-word phrases like "can't stop thinking" or
"walking on eggshells" against the user's text.
"""

import spacy

nlp = spacy.load("en_core_web_sm")


def process(text: str):
    """Lowercase, tokenize, lemmatize — same as Step 1."""
    text = text.lower()
    doc = nlp(text)
    return [t.lemma_ for t in doc if not t.is_punct and not t.is_space]


def generate_ngrams(tokens, max_n=4):
    """
    Generate all contiguous n-grams from length 1 up to max_n.

    Returns a list of tuples of tokens.
    Example for ['i', 'can', 'not', 'stop']:
      length 1: ('i',), ('can',), ('not',), ('stop',)
      length 2: ('i','can'), ('can','not'), ('not','stop')
      length 3: ('i','can','not'), ('can','not','stop')
      length 4: ('i','can','not','stop')
    """
    ngrams = []
    for n in range(1, max_n + 1):
        for i in range(len(tokens) - n + 1):
            ngrams.append(tuple(tokens[i:i + n]))
    return ngrams


if __name__ == "__main__":
    sentence = (
        "Lately I can't sleep and I keep replaying that conversation "
        "in my head. I'm so tired."
    )

    tokens = process(sentence)
    print("Tokens:")
    print(tokens)
    print()

    ngrams = generate_ngrams(tokens, max_n=4)

    # Group by size for readability
    for n in range(1, 5):
        group = [g for g in ngrams if len(g) == n]
        print(f"--- {n}-grams ({len(group)}) ---")
        for g in group:
            print("  " + " ".join(g))
        print()

    print("Total n-grams:", len(ngrams))