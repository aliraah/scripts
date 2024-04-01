import pymongo
import sys
from pymongo.errors import DuplicateKeyError

subdomains_textfile = sys.argv[1]
organisation = sys.argv[2] 

if len(sys.argv) >= 4:
    found_by = sys.argv[3] 
else:
    found_by = "subfinder"

# Function to read subdomains from file and insert into MongoDB
def insert_subdomains(filename):
    # Connect to MongoDB
    client = pymongo.MongoClient("<CONNECTION-STRING")
    db = client["assets"]
    collection = db[f"{organisation}"]

    # Create a unique index on the "subdomain" field
    collection.create_index("subdomain", unique=True)
    
    # Open file and read subdomains
    with open(filename, 'r') as file:
        subdomains = file.readlines()
        num_subdomains = 0 
        # Insert each subdomain into MongoDB
        for subdomain in subdomains:
            subdomain = subdomain.strip()  # Remove leading/trailing whitespace
            doc = {"subdomain": subdomain, "org": organisation, "found_by": found_by, "x_status_code": ""}
            try:
                collection.insert_one(doc)
                num_subdomains += 1
            except DuplicateKeyError:
                print(f"Skipping duplicate subdomain: {subdomain}")
                continue

    print(f"{num_subdomains} subdomains inserted into {organisation} collection.")

insert_subdomains(subdomains_textfile)
