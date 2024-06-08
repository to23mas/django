"""storage for projects"""
from pymongo.cursor import Cursor
from domain.Mongo import MongoStorage


def find_projects_by_course(course: str) -> Cursor:
    ms = MongoStorage()
    return ms.database[course].projects.find().sort('no')


def find_projects_by_course_and_ids(ids: list, course: str) -> Cursor:
    ms = MongoStorage()
    return ms.database[course].projects.find({"no": {"$in": ids}}).sort('no')


def get_project_detail(project_no: int, course: str):
    ms = MongoStorage()
    return ms.database[course].projects.find_one(
        {"no": project_no},
        {'no': 1, 'lessons': 1, 'title': 1, 'card': {'description':1}})


def get_locked_projects(username: str):
    ms = MongoStorage()
    return ms.database.progress.find_one({"_id": username}, {"projects": 1})
