use("psych_support")

db.symptoms.updateMany(
  { "weights.rumination": { $exists: true } },
  { $addToSet: { problems: "rumination" } }
)
db.symptoms.updateMany(
  { "weights.procrastination": { $exists: true } },
  { $addToSet: { problems: "procrastination" } }
)
db.symptoms.updateMany(
  { "weights.self_criticism": { $exists: true } },
  { $addToSet: { problems: "self_criticism" } }
)
db.symptoms.updateMany(
  { "weights.burnout": { $exists: true } },
  { $addToSet: { problems: "burnout" } }
)
db.symptoms.updateMany(
  { "weights.avoidance": { $exists: true } },
  { $addToSet: { problems: "avoidance" } }
)
print("Tagged. Sample:")
db.symptoms.find({ problems: { $exists: true } }).limit(1).forEach(d => printjson(d))