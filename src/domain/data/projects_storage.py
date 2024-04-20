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
    return ms.database.projects.find_one(
        {"_id": project_id},
        {'lessons': 1, 'title': 1, 'card': {'description':1}})


def get_lesson(lesson_id: int):
    ms = MongoStorage()
    return ms.database.lessons.find_one({"_id": lesson_id})


def get_chapter(chapter_id: int):
    ms = MongoStorage()
    return ms.database.chapters.find_one({"_id": chapter_id})


def get_progress_projects(username: str):
    ms = MongoStorage()
    return ms.database.progress.find_one({"_id": username})


def get_lesson_progress(username: str, project_id: int):
    ms = MongoStorage()
    return ms.database.progress.find_one(
        {"_id": username, f'lessons.{project_id}': {'$exists': True}},
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
