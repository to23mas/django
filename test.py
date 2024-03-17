from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.inpv
projects = list(db.projects.find())

print(projects)
# for project in projects.find():
#     print(project)

# from src.domain.data.projects_storage import ProjectsStorage

# ms = MongoStorage()
# db = ms.client.inpv
# project = db.projects.find()
#
# print(project)
# ProjectsStorage.findTitles()
# get_projects()
