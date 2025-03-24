from unittest import TestCase
from unittest.mock import MagicMock
from domain.data.tests.TestData import TestData
from domain.data.tests.TestStorage import TestStorage
from domain.data.tests.TestDataCollection import TestDataCollection

class TestTestStorage(TestCase):
	def setUp(self):
		self.mock_db = MagicMock()
		self.storage = TestStorage()
		self.storage.database = {'test_db': self.mock_db}
		self.test_test = TestData(
			id=1,
			title="Test Test",
			time=60,
			description="Test Description",
			unlock_lesson=1,
			unlock_chapter=1,
			unlock_project=1,
			finish_project=1,
			finish_lesson=1,
			finish_chapter=1,
			attempts=3,
			success_score=70.0,
			total_points=100
		)

	def test_get_test(self):
		mock_test = {
			"_id": 1,
			"title": "Test Test",
			"time": 60,
			"description": "Test Description",
			"unlock_lesson": 1,
			"unlock_chapter": 1,
			"unlock_project": 1,
			"finish_project": 1,
			"finish_lesson": 1,
			"finish_chapter": 1,
			"attempts": 3,
			"success_score": 70.0,
			"total_points": 100,
			"questions": None
		}
		self.mock_db.tests.find_one.return_value = mock_test

		result, questions = self.storage.get_test('test_db', 1)
		self.assertEqual(result.id, 1)
		self.assertEqual(result.title, "Test Test")
		self.assertIsNone(questions)
		self.mock_db.tests.find_one.assert_called_once_with({"_id": 1})

	def test_get_test_not_found(self):
		self.mock_db.tests.find_one.return_value = None
		with self.assertRaises(Exception):
			self.storage.get_test('test_db', 1)

	def test_find_tests_for_overview(self):
		mock_tests = [
			{
				"_id": 1,
				"title": "Test Test 1",
				"time": 60,
				"description": "Test Description 1",
				"unlock_lesson": 1,
				"unlock_chapter": 1,
				"unlock_project": 1,
				"finish_project": 1,
				"finish_lesson": 1,
				"finish_chapter": 1,
				"attempts": 3,
				"success_score": 70.0,
				"total_points": 100
			},
			{
				"_id": 2,
				"title": "Test Test 2",
				"time": 60,
				"description": "Test Description 2",
				"unlock_lesson": 1,
				"unlock_chapter": 1,
				"unlock_project": 1,
				"finish_project": 1,
				"finish_lesson": 1,
				"finish_chapter": 1,
				"attempts": 3,
				"success_score": 70.0,
				"total_points": 100
			}
		]
		mock_find = MagicMock()
		mock_sort = MagicMock()
		mock_sort.__iter__ = lambda _: iter(mock_tests)
		mock_find.sort.return_value = mock_sort
		self.mock_db.tests.find.return_value = mock_find

		result = self.storage.find_tests_for_overview('test_db', [1, 2])
		self.assertEqual(len(result), 2)
		self.assertEqual(result[0].id, 1)
		self.assertEqual(result[1].id, 2)
		self.mock_db.tests.find.assert_called_once()

	def test_create_test(self):
		self.storage.create_test(self.test_test, 'test_db')
		self.mock_db.tests.insert_one.assert_called_once()

	def test_delete_test(self):
		self.storage.delete_test('test_db', 1)
		self.mock_db.tests.delete_one.assert_called_once_with({"_id": 1})

	def test_update_test(self):
		self.storage.update_test(self.test_test, 'test_db')
		self.mock_db.tests.update_one.assert_called_once()

	def test_get_next_valid_id(self):
		mock_document = {"_id": 5}
		self.mock_db.tests.find_one.return_value = mock_document
		result = self.storage.get_next_valid_id('test_db')
		self.assertEqual(result, 6)

	def test_get_next_valid_id_no_documents(self):
		self.mock_db.tests.find_one.return_value = None
		result = self.storage.get_next_valid_id('test_db')
		self.assertEqual(result, 1)

class TestTestDataCollection(TestCase):
	def test_from_dict(self):
		mock_data = [
			{
				"_id": 1,
				"title": "Test Test 1",
				"time": 60,
				"description": "Test Description 1",
				"unlock_lesson": 1,
				"unlock_chapter": 1,
				"unlock_project": 1,
				"finish_project": 1,
				"finish_lesson": 1,
				"finish_chapter": 1,
				"attempts": 3,
				"success_score": 70.0,
				"total_points": 100
			}
		]
		result = TestDataCollection.from_array(mock_data)
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0].id, 1)
		self.assertEqual(result[0].title, "Test Test 1")
