import pymongo
import json
import sys

metadata_textfile = sys.argv[1]
col = sys.argv[2]

# Function to update documents in MongoDB based on input key
def update_documents(filename):
    # Connect to MongoDB
    client = pymongo.MongoClient("<CONNECTION-STRING>")
    db = client["assets"]
    collection = db[f"{col}"]

    # Open file and read information
    with open(filename, 'r') as file:
        for line in file:
            data = json.loads(line)
            input_key = data.get("input")
            if input_key:
                # Find document in MongoDB collection with matching input key and update it
                collection.update_one({"subdomain": input_key}, {"$set": data}, upsert=True)

    print("Documents updated in MongoDB.")

update_documents(metadata_textfile)
