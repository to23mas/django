"""storage for projects"""
from pymongo.cursor import Cursor
from domain.Mongo import MongoStorage

def get_lesson(lesson_no: str, project_no: str, course: str) -> dict | None:
    ms = MongoStorage()
    return ms.database[course].lessons.find_one({
        "no": int(lesson_no),
        "project": int(project_no),
    })

