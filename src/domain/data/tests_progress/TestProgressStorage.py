"""storage for progress"""
from domain.Mongo import MongoStorage
from domain.data.tests.enum.TestState import TestState
from domain.data.tests_progress.TestProgressData import TestProgressData
from domain.data.tests_progress.TestProgressDataSerializer import TestProgressDataSerializer


def get_test_progress(db: str, username: str, test_id: int) -> TestProgressData | None:
	"""return user's one test progress"""
	result =  MongoStorage().database[db].progress.find_one(
		{ '_id': username, 'tests.test_id': test_id},
		{ 'tests.$': 1, '_id': 0 })

	if result != None:
		return TestProgressDataSerializer.from_dict(result['tests'][0])
	return result

def update_test_progress(course: str, username: str, test_no: str, score: float, state: TestState) -> dict | None:
	MongoStorage().database[course].progress.update_one(
		{'_id': username, 'tests.test_no': int(test_no)},
		{
			'$push': { 'tests.$.score': score },
			'$set': { 'tests.$.state': state.value }
		}, upsert=False)
