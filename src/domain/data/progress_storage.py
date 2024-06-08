"""storage for progress"""
from pymongo.cursor import Cursor
from domain.Mongo import MongoStorage


def get_user_progress_by_course(username: str, course: str):
    ms = MongoStorage()
    return ms.database[course].progress.find_one({"_id": username})

def get_lesson_progress(username: str, project_no: int, course: str):
    ms = MongoStorage()
    return ms.database[course].progress.find_one(
        {"_id": username, f'lessons.{str(project_no)}': {'$exists': True}},
        {'lessons': 1})

