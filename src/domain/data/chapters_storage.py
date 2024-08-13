"""storage for projects"""
from pymongo.cursor import Cursor
from domain.Mongo import MongoStorage




def is_chapter_open_or_done(username: str, course: str, project_no: str, lesson_no: str, chapter_no: str) -> bool:
    ms = MongoStorage()
    return ms.database[course].progress.count_documents({
        '_id': username,
        '$or': [{"projects.done": int(project_no)},
                {"projects.open": int(project_no)}],
        '$or': [{f"lessons.{project_no}.done": int(lesson_no)},
                {f"lessons.{project_no}.open": int(lesson_no)}],
        '$or': [{f"chapters.{lesson_no}.open": int(chapter_no)},
                {f"chapters.{lesson_no}.done": int(chapter_no)}],
    }) == 1
