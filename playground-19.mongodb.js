use("psych_support")

print("Total:", db.symptoms.countDocuments())
print("Missing problems field:", db.symptoms.countDocuments({ problems: { $exists: false } }))
print("rumination:", db.symptoms.countDocuments({ problems: "rumination" }))
print("procrastination:", db.symptoms.countDocuments({ problems: "procrastination" }))
print("self_criticism:", db.symptoms.countDocuments({ problems: "self_criticism" }))
print("Shared (in 2+ problems):", db.symptoms.countDocuments({ $expr: { $gte: [{ $size: "$problems" }, 2] } }))