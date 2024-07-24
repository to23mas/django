"""storage for tests and its data. data about tests"""
import pymongo
from typing import Tuple, List
from domain.Mongo import MongoStorage
from domain.data.exception.DataNotFoundException import DataNotFoundException
from domain.data.tests.QuestionData import QuestionData
from domain.data.tests.QuestionDataCollection import QuestionDataCollection
from domain.data.tests.TestDataCollection import TestDataCollection
from domain.data.tests.TestDataSerializer import TestDataSerializer
from domain.data.tests.TestData import TestData


def find_tests_for_overview(db: str, open_tests: list = []) -> List[TestData]:
	"""returns all test"""
	tests = MongoStorage().database[db].tests.find(
		{'no': {'$in': open_tests}}).sort('no', pymongo.DESCENDING)

	if tests == None: raise DataNotFoundException

	return TestDataCollection.from_array(tests)


def get_test(db: str, test_id: int) -> Tuple[TestData | None, List[QuestionData] | None]:
	""" Return one test by its NO. Raises: DataNotFoundException"""

	test_data = MongoStorage().database[db].tests.find_one({'_id': test_id})

	if test_data == None:
		raise DataNotFoundException

	serialized_test_data =  TestDataSerializer().from_array(test_data)
	serialized_question_data_collection = QuestionDataCollection.from_array(test_data.get('questions'))

	return (serialized_test_data, serialized_question_data_collection)


def find_tests(db: str) -> List[TestData] | None:

	tests = MongoStorage().database[db].tests.find().sort('_id')
	match tests:
		case None: return tests
		case _: return TestDataCollection.from_array(tests)


