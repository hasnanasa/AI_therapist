from pymongo import MongoClient

# Connect to your local MongoDB
client = MongoClient("mongodb://localhost:27017")

# Point to the psych_support database
db = client["psych_support"]

# Count documents in each collection
print("Connected to MongoDB.")
print("Database: psych_support")
print("Problems collection:", db.problems.count_documents({}), "documents")
print("Symptoms collection:", db.symptoms.count_documents({}), "documents")