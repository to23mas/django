"""storage for progress"""
from pymongo.cursor import Cursor
from domain.Mongo import MongoStorage


def find_tests(course: str, open_tests: list = []) -> Cursor:
    """returns all test"""
    ms = MongoStorage()

    # if len(open_tests) == 0:
    #     return ms.database[course].tests.find()

    # TODO -> tohle by m2lo vrátit jen no->1  asi vrací dobře, jen to checkni
    return ms.database[course].tests.find({'no': {'$in': [1]}})

def get_test(course: str, test_no: str) -> dict | None:
    """returns one test by its NO"""
    ms = MongoStorage()

    return ms.database[course].tests.find_one({'no': int(test_no)})
