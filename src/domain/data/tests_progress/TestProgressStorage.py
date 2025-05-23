"""storage for progress"""
import datetime
from domain.Mongo import MongoStorage
from domain.data.tests.enum.TestState import TestState
from domain.data.tests_progress.TestProgressData import TestProgressData
from domain.data.tests_progress.TestProgressDataSerializer import TestProgressDataSerializer


class TestProgressStorage(MongoStorage):
	def __init__(self):
		super().__init__()


	def get_test_progress(self, db: str, username: str, test_id: int) -> TestProgressData | None:
		"""return user's one test progress"""
		result =  self.database[db].progress.find_one(
			{ '_id': username, 'tests.test_id': test_id},
			{ 'tests.$': 1, '_id': 0 })

		if result is not None:
			return TestProgressDataSerializer.from_dict(result['tests'][0])
		return result


	def update_test_progress(self, db: str, username: str, test_id: int, score: float, state: TestState, attempts: int) -> dict | None:
		match (attempts):
			case 0: lock_until =  datetime.datetime.now() + datetime.timedelta(minutes=15)
			case _: lock_until = ''

		self.database[db].progress.update_one(
			{'_id': username, 'tests.test_id': test_id},
			{
				'$push': { 'tests.$.score': score },
				'$set': {
					'tests.$.state': state.value,
					'tests.$.attempts': attempts,
					'tests.$.lock_until': lock_until
				}
			}, upsert=False)

	def reset_lock(self, db: str, username: str, test_id: int, attempts: int) -> None:
		self.database[db].progress.update_one(
			{'_id': username, 'tests.test_id': test_id},
			{'$set': {
				'tests.$.lock_until': '',
				'tests.$.attempts': attempts,
			}}, upsert=False)


	def unlock_test(self, db: str, username: str, test_id: int, state: TestState) -> dict | None:
		self.database[db].progress.update_one(
			{'_id': username, 'tests.test_id': test_id},
			{
				'$set': { 'tests.$.state': state.value }
			}, upsert=False)
