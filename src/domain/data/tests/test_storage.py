"""storage for progress"""
from pymongo.cursor import Cursor
from domain.Mongo import MongoStorage
from domain.data.tests_progress.test_progress_data import TestProgress
from domain.data.tests_progress.test_progress_serializer import TestProgressSerializer


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


def get_tests_progress(course: str, username: str, test_no: str) -> TestProgress | None:
    """return user's one test progress"""
    result =  MongoStorage().database[course].progress.find_one(
        { '_id': username, 'tests.test_no': int(test_no)},
        { 'tests.$': 1, '_id': 0 })

    if result != None:
         return TestProgressSerializer.from_array(result['tests'][0])
    return result




