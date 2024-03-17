"""storage for projects"""
from domain.Mongo import MongoStorage
from bson.objectid import ObjectId


class ProjectsStorage():

    def findOverviews() -> list:
        ms = MongoStorage()
        return ms.database.projects.find()

    def getDetail(project_no: int) -> list:
        ms = MongoStorage()
        return ms.database.projects.find_one({"no": project_no})
