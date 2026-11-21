use("psych_support")

db.problems.insertMany([
  {
    name: "rumination",
    display_name: "Rumination / Overthinking",
    description: "Replaying thoughts over and over, can't stop thinking"
  },
  {
    name: "procrastination",
    display_name: "Procrastination",
    description: "Can't start tasks, keeps delaying, puts things off"
  },
  {
    name: "self_criticism",
    display_name: "Self-Criticism",
    description: "Harsh judgment of self, feeling not good enough"
  },
  {
    name: "burnout",
    display_name: "Burnout",
    description: "Exhaustion, drained, no energy, can't keep going"
  },
  {
    name: "avoidance",
    display_name: "Avoidance",
    description: "Dodging situations, people, or feelings"
  }
])

print("Problems in database:", db.problems.countDocuments())
db.problems.find().forEach(p => print("- " + p.name))