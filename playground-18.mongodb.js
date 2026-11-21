use("psych_support")

db.symptoms.createIndex(
  { phrase: "text", variants: "text" },
  { weights: { phrase: 10, variants: 5 }, name: "phrase_search" }
)

print("Indexes:")
db.symptoms.getIndexes().forEach(i => print("  " + i.name))