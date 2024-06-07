"""storage for projects"""
from pymongo.cursor import Cursor
from domain.Mongo import MongoStorage


def find_projects(course: str) -> Cursor:
    ms = MongoStorage()
    return ms.database.projects[course].find()


def find_projects_in(ids: list, course: str) -> Cursor:
    ms = MongoStorage()
    return ms.database.projects[course].find({"no": {"$in": ids}})


def get_project_detail(project_no: int, course: str):
    ms = MongoStorage()
    return ms.database.projects[course].find_one(
        {"no": project_no},
        {'no': 1, 'lessons': 1, 'title': 1, 'card': {'description':1}})


def get_lesson(lesson_no: int, course: str):
    ms = MongoStorage()
    return ms.database.lessons[course].find_one({"no": lesson_no})


def get_chapter(chapter_no: int, course: str):
    ms = MongoStorage()
    return ms.database.chapters[course].find_one({"no": chapter_no})


def chapter_is_accessible_and_done(username: str, course: str, project_no: str, lesson_no: str, chapter_no: str) -> bool:
    ms = MongoStorage()
    return ms.database.progress[course].count_documents({
        '_id': username,
        '$or': [{"projects.done": int(project_no)},
                {"projects.open": int(project_no)}],
        '$or': [{f"lessons.{project_no}.done": int(lesson_no)},
                {f"lessons.{project_no}.open": int(lesson_no)}],
        f"chapters.{lesson_no}.done": int(chapter_no)
    }) == 1

def is_chapter_open(username: str, course: str, project_no: str, lesson_no: str, chapter_no: str) -> bool:
    ms = MongoStorage()
    return ms.database.progress[course].count_documents({
        '_id': username,
        '$or': [{"projects.done": int(project_no)},
                {"projects.open": int(project_no)}],
        '$or': [{f"lessons.{project_no}.done": int(lesson_no)},
                {f"lessons.{project_no}.open": int(lesson_no)}],
        '$or': [{f"chapters.{lesson_no}.open": int(chapter_no)},
                {f"chapters.{lesson_no}.done": int(chapter_no)}],
    }) == 1


def get_progress_projects(username: str, course: str):
    ms = MongoStorage()
    return ms.database.progress[course].find_one({"_id": username})


def get_lesson_progress(username: str, project_no: int, course: str):
    ms = MongoStorage()
    return ms.database.progress[course].find_one(
        {"_id": username, f'lessons.{str(project_no)}': {'$exists': True}},
        {'lessons': 1})


def get_locked_projects(username: str):
    ms = MongoStorage()
    return ms.database.progress.find_one({"_id": username}, {"projects": 1})


def unlock_project(username: str, project_id: int, unlock: bool):
    """ if not unlock -> complete """
    ms = MongoStorage()

    to_add = 'open' if unlock else 'done'
    to_rem = 'lock' if unlock else 'open'

    ms.database.progress.update_one(
        {
            '_id': username
        },{
            '$push': {f'projects.{to_add}': project_id},
            '$pull': {f'projects.{to_rem}': project_id}
        })


def progress_lesson_or_chapter(username: str, updated_item_id: int, parent_id: int, unlock: bool, lesson: bool):
    """ if not unlock -> complete, if not lesson -> chapter """
    ms = MongoStorage()

    to_add = 'open' if unlock else 'done'
    to_rem = 'lock' if unlock else 'open'
    repository = 'lessons' if lesson else 'chapters'

    ms.database.progress.update_one(
        {
            '_id': username
        },{
            '$push': {f'{repository}.{parent_id}.{to_add}': updated_item_id},
            '$pull': {f'{repository}.{parent_id}.{to_rem}': updated_item_id},
        })
