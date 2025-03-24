from unittest import TestCase
from unittest.mock import MagicMock
from domain.data.lessons.LessonData import LessonData
from domain.data.lessons.LessonStorage import LessonStorage
from domain.data.lessons.LessonDataCollection import LessonDataCollection

class TestLessonStorage(TestCase):
	def setUp(self):
		self.mock_lessons = MagicMock()
		self.mock_project_db = MagicMock()
		self.mock_project_db.lessons = self.mock_lessons
		self.mock_project = MagicMock()
		self.mock_project.__getitem__.return_value = self.mock_project_db
		self.mock_db = MagicMock()
		self.mock_db.project = self.mock_project
		self.storage = LessonStorage()
		self.storage.database = {'test_db': self.mock_db}
		self.test_lesson = LessonData(
			id=1,
			title="Test Lesson",
			to=[2, 3]
		)

	def test_get_lesson(self):
		mock_lesson = {
			"_id": 1,
			"title": "Test Lesson",
			"to": [2, 3]
		}
		self.mock_lessons.find_one.return_value = mock_lesson

		result = self.storage.get_lesson(1, 'test_db', 'project_db')
		self.assertEqual(result.id, 1)
		self.assertEqual(result.title, "Test Lesson")
		self.mock_lessons.find_one.assert_called_once_with({"_id": 1})

	def test_get_lesson_not_found(self):
		self.mock_lessons.find_one.return_value = None
		result = self.storage.get_lesson(1, 'test_db', 'project_db')
		self.assertIsNone(result)

	def test_find_lessons(self):
		mock_lessons = [
			{
				"_id": 1,
				"title": "Test Lesson 1",
				"to": [2, 3]
			},
			{
				"_id": 2,
				"title": "Test Lesson 2",
				"to": [3, 4]
			}
		]
		mock_find = MagicMock()
		mock_sort = MagicMock()
		mock_sort.__iter__ = lambda _: iter(mock_lessons)
		mock_find.sort.return_value = mock_sort
		self.mock_lessons.find.return_value = mock_find

		result = self.storage.find_lessons('test_db', 'project_db')
		self.assertEqual(len(result), 2)
		self.assertEqual(result[0].id, 1)
		self.assertEqual(result[1].id, 2)
		self.mock_lessons.find.assert_called_once()
		mock_find.sort.assert_called_once_with('_id')

	def test_create_lesson(self):
		self.storage.create_lesson(self.test_lesson, 'test_db', 'project_db')
		self.mock_lessons.insert_one.assert_called_once()

	def test_delete_lesson(self):
		self.storage.delete_lesson('test_db', 'project_db', 1)
		self.mock_lessons.delete_one.assert_called_once_with({"_id": 1})

	def test_update_lesson(self):
		self.storage.update_lesson(self.test_lesson, 'test_db', 'project_db')
		self.mock_lessons.update_one.assert_called_once()

	def test_get_next_valid_id(self):
		mock_document = {"_id": 5}
		self.mock_lessons.find_one.return_value = mock_document
		result = self.storage.get_next_valid_id('test_db', 'project_db')
		self.assertEqual(result, 6)

	def test_get_next_valid_id_no_documents(self):
		self.mock_lessons.find_one.return_value = None
		result = self.storage.get_next_valid_id('test_db', 'project_db')
		self.assertEqual(result, 1)

	def test_find_lessons_by_course(self):
		mock_lessons = [
			{
				"_id": 1,
				"title": "Test Lesson 1",
				"to": [2, 3]
			}
		]
		mock_find = MagicMock()
		mock_find.__iter__ = lambda _: iter(mock_lessons)
		self.mock_lessons.find.return_value = mock_find

		result = self.storage.find_lessons_by_course('test_db', 'project_db')
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0].id, 1)
		self.mock_lessons.find.assert_called_once()

class TestLessonDataCollection(TestCase):
	def test_from_dict(self):
		mock_data = [
			{
				"_id": 1,
				"title": "Test Lesson 1",
				"to": [2, 3]
			}
		]
		result = LessonDataCollection.from_dict(mock_data)
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0].id, 1)
		self.assertEqual(result[0].title, "Test Lesson 1")
