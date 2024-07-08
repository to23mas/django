"""storage for progress"""
from typing import List

import pymongo
from domain.Mongo import MongoStorage
from domain.data.tests.test_data import TestData
from domain.data.tests.tests_data_collection import TestCollection


def find_tests_for_overview(course: str, open_tests: list = []) -> List[TestData]:
    """returns all test"""
    tests = MongoStorage().database[course].tests.find(
        {'no': {'$in': open_tests}},
        {"questions": 0}).sort('no', pymongo.DESCENDING)

    return TestCollection.from_array(tests) #type: ignore

def get_test(course: str, test_no: str) -> dict | None:
    """returns one test by its NO"""
    ms = MongoStorage()

    return ms.database[course].tests.find_one({'no': int(test_no)})
