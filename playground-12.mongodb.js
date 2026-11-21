use("psych_support")

print("Total:", db.symptoms.countDocuments())
print("rumination:", db.symptoms.countDocuments({ "weights.rumination": { $exists: true } }))
print("procrastination:", db.symptoms.countDocuments({ "weights.procrastination": { $exists: true } }))
print("self_criticism:", db.symptoms.countDocuments({ "weights.self_criticism": { $exists: true } }))