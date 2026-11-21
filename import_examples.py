"""
import_examples.py — read seed_examples.txt and insert the
examples into MongoDB as documents in the `example_texts` collection.

File format expected:
    ### burnout
    example one
    example two
    ...
    ### procrastination
    example one
    ...
"""

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["psych_support"]

# ─────────────────────────────────────────────────────────────
# 1. Read and parse the file
# ─────────────────────────────────────────────────────────────

with open("seed_examples.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Parse into { problem: [example, example, ...] }
problems = {}
current_problem = None

prefixes = {
    "burnout": "bur",
    "procrastination": "pro",
    "self_criticism": "sel",
    "rumination": "rum",
    "avoidance": "avo",
}

for line in lines:
    line = line.strip()
    if not line:
        continue
    if line.startswith("###"):
        # Extract the problem name after "###"
        current_problem = line.replace("###", "").strip().lower()
        problems[current_problem] = []
    elif current_problem:
        problems[current_problem].append(line)

# Report what was parsed
print("Parsed from seed_examples.txt:")
for p, examples in problems.items():
    print(f"  {p}: {len(examples)} examples")
print()

# ─────────────────────────────────────────────────────────────
# 2. Clear old examples (safe re-run)
# ─────────────────────────────────────────────────────────────

db.example_texts.delete_many({})
print("Cleared existing example_texts collection.\n")

# ─────────────────────────────────────────────────────────────
# 3. Build documents and insert
# ─────────────────────────────────────────────────────────────

documents = []
for problem, examples in problems.items():
    prefix = prefixes.get(problem, "unk")
    for i, text in enumerate(examples, start=1):
        documents.append({
            "_id": f"{prefix}_ex_{i:03d}",
            "text": text,
            "problem": problem,
            "source": "own_writing",
        })

if documents:
    result = db.example_texts.insert_many(documents, ordered=False)
    print(f"Inserted {len(result.inserted_ids)} documents.")
else:
    print("No documents to insert.")

# ─────────────────────────────────────────────────────────────
# 4. Verify
# ─────────────────────────────────────────────────────────────

print("\nVerification:")
print("Total example_texts:", db.example_texts.count_documents({}))
for problem in prefixes.keys():
    count = db.example_texts.count_documents({"problem": problem})
    print(f"  {problem}: {count}")