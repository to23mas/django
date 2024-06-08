"""storage for progress"""
from pymongo.cursor import Cursor
from domain.Mongo import MongoStorage


def find_tests(course: str) -> Cursor:
    """returns all test"""
    ms = MongoStorage()

    return ms.database[course].tests.find()


def get_test(course: str, test_no: str) -> dict | None:
    """returns one test by its NO"""
    ms = MongoStorage()

    return ms.database[course].tests.find_one({'no': int(test_no)})
