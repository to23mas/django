"""storage for progress"""
from domain.Mongo import MongoStorage
from domain.data.tests_progress.TestProgressData import TestProgressData
from domain.data.tests_progress.TestProgressDataSerializer import TestProgressDataSerializer


def get_test_progress(course: str, username: str, test_no: str) -> TestProgressData | None:
    """return user's one test progress"""
    result =  MongoStorage().database[course].progress.find_one(
        { '_id': username, 'tests.test_no': int(test_no)},
        { 'tests.$': 1, '_id': 0 })

    if result != None:
         return TestProgressDataSerializer.from_array(result['tests'][0])
    return result
