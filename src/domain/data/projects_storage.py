"""storage for projects"""
from domain.Mongo import MongoStorage


class ProjectsStorage():

    def findTitles() -> list:
        ms = MongoStorage()
        return ms.database.projects.find()
