from pymongo import MongoClient
from os import listdir
import json


dir = './db/migrations/documents/projects/'
files = listdir(dir)

client = MongoClient('localhost', 27017)
db = client.inpv
projects = db.projects

for file in files:
    with open(dir + file) as f:
        file_data = json.load(f)
        projects.insert_one(file_data)

client.close()
