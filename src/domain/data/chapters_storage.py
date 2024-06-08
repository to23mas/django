"""storage for projects"""
from pymongo.cursor import Cursor
from domain.Mongo import MongoStorage

def get_chapter(project_no: str, lesson_no: str, chapter_no: str, course: str):
    ms = MongoStorage()
    return ms.database[course].chapters.find_one({
        "no": chapter_no,
        "project": project_no,
        "lesson": lesson_no,
    })
