"""storage for projects"""
from pymongo.cursor import Cursor
from domain.Mongo import MongoStorage


def find_projects() -> Cursor:
    ms = MongoStorage()
    return ms.database.projects.find()


def find_projects_in(ids: list) -> Cursor:
    ms = MongoStorage()
    print(ids)
    return ms.database.projects.find({"no": {"$in": ids}})


def get_project_detail(project_id: int):
    ms = MongoStorage()
    return ms.database.projects.find_one({"_id": project_id})


def get_lesson(lesson_id: int):
    ms = MongoStorage()
    return ms.database.lessons.find_one({"_id": lesson_id})


def get_chapter(chapter_id: int):
    ms = MongoStorage()
    return ms.database.chapters.find_one({"_id": chapter_id})


def get_progress_projects(username: str):
    ms = MongoStorage()
    return ms.database.progress.find_one({"_id": username}, {"projects": 1})
