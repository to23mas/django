"""storage for progress"""
from pymongo.cursor import Cursor
from domain.Mongo import MongoStorage


def find_tests_for_overview(course: str, open_tests: list = []) -> Cursor:
    """returns all test"""
    ms = MongoStorage()

    return ms.database[course].tests.find(
        {'no': {'$in': open_tests}},
        {"questions": 0}
    )

def get_test(course: str, test_no: str) -> dict | None:
    """returns one test by its NO"""
    ms = MongoStorage()

    return ms.database[course].tests.find_one({'no': int(test_no)})
