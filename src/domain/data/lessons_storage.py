"""storage for projects"""
from pymongo.cursor import Cursor
from domain.Mongo import MongoStorage

def get_lesson(lesson_no: int, project_no: str, course: str) -> dict | None:
    ms = MongoStorage()
    return ms.database[course].lessons.find_one({
        "no": lesson_no,
        "project": project_no,
    })

