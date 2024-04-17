from pymongo import MongoClient
import subprocess
import os
import sys
import json

org = sys.argv[1]

client = MongoClient("<CONNECTION-STRING>")
db = client.assets
collection = db[f'{org}']


def query_subdomains():  
    documents = collection.find()
    
    with open("subdomains.txt", "w") as file:
        for document in documents:
            subdomain = document.get('subdomain')
            if subdomain:
                file.write(subdomain + "\n")
    
    run_dnsx("subdomains.txt")

def run_dnsx(filename):
    try:
        result = subprocess.run(['dnsx', '-silent', '-l', filename, '-o', 'dnsx.txt'], capture_output=True, text=True, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

    run_httpx("dnsx.txt")

def run_httpx(filename):
    try:
        result = subprocess.run(['httpx', '-l', filename, '-json', '-o', 'httpx.txt'], capture_output=True, text=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

    update_documents("httpx.txt")


def update_documents(filename):
    # Initialize count for updated documents
    updated_count = 0

    # Open file and read information
    with open(filename, 'r') as file:
        for line in file:
            data = json.loads(line)
            input_key = data.get("input")

            existing_doc = collection.find_one({"subdomain": input_key})
            x_status_code = existing_doc.get("status_code")
            data['x_status_code'] = x_status_code

            if input_key:
                # Find document in MongoDB collection with matching input key and update it
                result = collection.update_one({"subdomain": input_key}, {"$set": data}, upsert=True)
                updated_count += result.modified_count

    print(f"{updated_count} documents updated in {org}.")


query_subdomains()
os.remove("subdomains.txt")
os.remove("dnsx.txt")
os.remove("httpx.txt")
