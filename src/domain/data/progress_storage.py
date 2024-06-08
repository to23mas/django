"""storage for progress"""
from pymongo.cursor import Cursor
from domain.Mongo import MongoStorage


def get_user_progress_by_course(username: str, course: str) -> dict | None:
    ms = MongoStorage()
    return ms.database[course].progress.find_one({"_id": username})

def get_lesson_progress(username: str, project_no: int, course: str) -> dict | None:
    ms = MongoStorage()
    return ms.database[course].progress.find_one(
        {"_id": username, f'lessons.{str(project_no)}': {'$exists': True}},
        {'lessons': 1})

def unlock_project(username: str, project_id: int, unlock: bool) -> None:
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


def unlock_lesson(username: str, course: str, project_no: str, lesson_no: str) -> None:
    ms = MongoStorage()

    ms.database[course].progress.update_one(
        {'_id': username},
        {'$push': {f'lessons.{str(project_no)}.open': int(lesson_no)},
         '$pull': {f'lessons.{str(project_no)}.lock': int(lesson_no)}})


def unlock_chapter(username: str, course: str, lesson_no: str, chapter_no: str) -> None:
    ms = MongoStorage()

    ms.database[course].progress.update_one(
        {'_id': username},
        {'$push': {f'chapters.{str(lesson_no)}.open': int(chapter_no)},
         '$pull': {f'chapters.{str(lesson_no)}.lock': int(chapter_no)}})


def finish_chapter(username: str, course: str, lesson_no: str, chapter_no: str) -> None:
    ms = MongoStorage()
    ms.database[course].progress.update_one(
        {'_id': username},
        {'$push': {f'chapters.{str(lesson_no)}.done': int(chapter_no)},
         '$pull': {f'chapters.{str(lesson_no)}.open': int(chapter_no)}})


def find_tests(course: str) -> Cursor:
    """returns all test"""
    ms = MongoStorage()

    return ms.database[course].tests.find()


def get_test(course: str, test_no: str) -> dict | None:
    """returns one test by its NO"""
    ms = MongoStorage()

    return ms.database[course].tests.find_one({'no': int(test_no)})


def find_tests_progress(course: str, username: str) -> dict | None:
    """return user's all tests progress"""
    ms = MongoStorage()

    return ms.database[course].progress.find_one({'_id': username}, {'tests': 1})


def get_tests_progress(course: str, username: str, test_no: str) -> dict | None:
    """return user's one test progress"""
    ms = MongoStorage()

    return ms.database[course].progress.find_one({'_id': username}, {f'tests.{test_no}': 1})
