from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.inpv
projects = db.projects

for project in projects.find():
    print(project)
