"""storage for tests and its data. data about tests"""
from domain.data.tests.tableDefinition.TableDefinitions import TestsTable
import pymongo
from typing import Tuple, List
from domain.Mongo import MongoStorage
from domain.data.exception.DataNotFoundException import DataNotFoundException
from domain.data.tests.QuestionData import QuestionData
from domain.data.tests.QuestionDataCollection import QuestionDataCollection
from domain.data.tests.QuestionDataSerializer import QuestionDataSerializer
from domain.data.tests.TestDataCollection import TestDataCollection
from domain.data.tests.TestDataSerializer import TestDataSerializer
from domain.data.tests.TestData import TestData


def find_tests_for_overview(db: str, open_tests: list = []) -> List[TestData]: #pylint: disable=W0102
	"""returns all test"""
	tests = MongoStorage().database[db].tests.find(
		{TestsTable.ID.value: {'$in': open_tests}}
	).sort(TestsTable.ID.value, pymongo.DESCENDING)

	if tests is None: raise DataNotFoundException

	return TestDataCollection.from_array(tests)


def get_test(db: str, test_id: int) -> Tuple[TestData | None, List[QuestionData] | None]:
	""" Return one test by its NO. Raises: DataNotFoundException"""

	test_data = MongoStorage().database[db].tests.find_one({'_id': test_id})

	if test_data is None:
		raise DataNotFoundException

	serialized_test_data =  TestDataSerializer().from_dict(test_data)
	if test_data.get('questions') is None:
		serialized_question_data_collection = None
	else:
		serialized_question_data_collection = QuestionDataCollection.from_array(test_data.get('questions'))

	return (serialized_test_data, serialized_question_data_collection)


def create_test(test_data: TestData, db: str) -> None:
	MongoStorage().database[db].tests.insert_one(TestDataSerializer.to_dict(test_data))


def create_question(question_data: QuestionData, test_id: int, db: str) -> None:
	MongoStorage().database[db].tests.update_one(
		{'_id': test_id},
		{'$push': {'questions': QuestionDataSerializer.to_dict(question_data)}}
	)


def find_tests(db: str) -> List[TestData] | None:
	tests = MongoStorage().database[db].tests.find().sort('_id')
	match tests:
		case None: return tests
		case _: return TestDataCollection.from_array(tests)


def exists_test(db: str, lesson_id: int) -> bool:
	res = MongoStorage().database[db].lessons.find_one({'_id': lesson_id})
	return res is not None


def delete_test(db: str, test_id: int) -> None:
	MongoStorage().database[db].tests.delete_one({'_id': test_id})


def get_next_valid_id(db: str) -> int:
	document = MongoStorage().database[db].tests.find_one(sort=[('_id', -1)])
	match document:
		case None: return 1
		case _: return document['_id'] + 1


def get_next_valid_question_id(db: str, test_id: int) -> int:
	pipeline = [
		{'$match': {'_id': test_id}},  # Match the document with the specified _id
		{'$unwind': '$questions'},  # Deconstruct the questions array
		{'$group': {'_id': None, 'max_question_id': {'$max': '$questions._id'}}}  # Group and find the maximum _id
	]
	result = list(MongoStorage().database[db].tests.aggregate(pipeline))

	if result:
		return result[0]['max_question_id'] + 1
	return 1


def update_test(test_data: TestData, db: str) -> None:
	MongoStorage().database[db].tests.update_one(
		{'_id': test_data.id},
		{'$set': TestDataSerializer.to_dict(test_data)}
	)


def update_question(question_data: QuestionData, db: str, test_id: int) -> None:
	MongoStorage().database[db].tests.update_one(
		{'_id': test_id, 'questions._id': question_data.id},
		{'$set': {
			'questions.$.question': question_data.question,
			'questions.$.type': question_data.type,
			'questions.$.points': question_data.points,
			'questions.$.answers': question_data.answers,
			'questions.$.correct': question_data.correct
		}}
	)


def delete_question(db: str, test_id: int, question_id: int) -> None:
	MongoStorage().database[db].tests.update_one(
		{'_id': test_id},
		{'$pull': {'questions': {'_id': question_id}}}
	)
