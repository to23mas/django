from unittest import TestCase
from unittest.mock import MagicMock
from domain.data.chapters.ChapterData import ChapterData
from domain.data.chapters.ChapterStorage import ChapterStorage
from domain.data.chapters.ChapterDataCollection import ChapterDataCollection

class TestChapterStorage(TestCase):
	def setUp(self):
		self.mock_chapters = MagicMock()
		self.mock_project_db = MagicMock()
		self.mock_project_db.chapters = self.mock_chapters
		self.mock_project = MagicMock()
		self.mock_project.__getitem__.return_value = self.mock_project_db
		self.mock_db = MagicMock()
		self.mock_db.project = self.mock_project
		self.storage = ChapterStorage()
		self.storage.database = {'test_db': self.mock_db}
		self.test_chapter = ChapterData(
			id=1,
			lesson_id=1,
			title="Test Chapter",
			unlock_type="none",
			unlock_id=0,
			unlocker_id=0,
			is_last_in_lesson=False,
			blocks=[]
		)

	def test_get_chapter(self):
		mock_chapter = {
			"_id": 1,
			"lesson_id": 1,
			"title": "Test Chapter",
			"unlock_type": "none",
			"unlock_id": 0,
			"unlocker_id": 0,
			"is_last_in_lesson": False,
			"blocks": []
		}
		self.mock_chapters.find_one.return_value = mock_chapter

		result = self.storage.get_chapter(1, 1, 'test_db', 'project_db')
		self.assertEqual(result.id, 1)
		self.assertEqual(result.title, "Test Chapter")
		self.mock_chapters.find_one.assert_called_once_with({
			"_id": 1,
			"lesson_id": 1
		})

	def test_get_chapter_not_found(self):
		self.mock_chapters.find_one.return_value = None
		result = self.storage.get_chapter(1, 1, 'test_db', 'project_db')
		self.assertIsNone(result)

	def test_find_chapters(self):
		mock_chapters = [
			{
				"_id": 1,
				"lesson_id": 1,
				"title": "Test Chapter 1",
				"unlock_type": "none",
				"unlock_id": 0,
				"unlocker_id": 0,
				"is_last_in_lesson": False,
				"blocks": []
			},
			{
				"_id": 2,
				"lesson_id": 1,
				"title": "Test Chapter 2",
				"unlock_type": "none",
				"unlock_id": 0,
				"unlocker_id": 0,
				"is_last_in_lesson": True,
				"blocks": []
			}
		]
		mock_find = MagicMock()
		mock_sort = MagicMock()
		mock_sort.__iter__ = lambda _: iter(mock_chapters)
		mock_find.sort.return_value = mock_sort
		self.mock_chapters.find.return_value = mock_find

		result = self.storage.find_chapters('test_db', 'project_db')
		self.assertEqual(len(result), 2)
		self.assertEqual(result[0].id, 1)
		self.assertEqual(result[1].id, 2)
		self.mock_chapters.find.assert_called_once_with({})
		mock_find.sort.assert_called_once_with('_id')

	def test_create_chapter(self):
		self.storage.create_chapter(self.test_chapter, 'test_db', 'project_db')
		self.mock_chapters.insert_one.assert_called_once_with({
			'_id': 1,
			'title': 'Test Chapter',
			'lesson_id': 1,
			'unlock_type': 'none',
			'unlock_id': 0,
			'unlocker_id': 0,
			'is_last_in_lesson': False,
			'blocks': []
		})

	def test_delete_chapter(self):
		self.storage.delete_chapter('test_db', 'project_db', 1, 1)
		self.mock_chapters.delete_one.assert_called_once_with({
			"_id": 1,
			"lesson_id": 1
		})

	def test_update_chapter(self):
		self.storage.update_chapter(self.test_chapter, 'test_db', 'project_db', 1)
		self.mock_chapters.update_one.assert_called_once_with(
			{
				"_id": self.test_chapter.id,
				"lesson_id": 1
			},
			{'$set': {
				'_id': 1,
				'title': 'Test Chapter',
				'lesson_id': 1,
				'unlock_type': 'none',
				'unlock_id': 0,
				'unlocker_id': 0,
				'is_last_in_lesson': False,
				'blocks': []
			}}
		)

	def test_get_next_valid_id(self):
		mock_document = {"_id": 5}
		self.mock_chapters.find_one.return_value = mock_document
		result = self.storage.get_next_valid_id('test_db', 'project_db')
		self.assertEqual(result, 6)
		self.mock_chapters.find_one.assert_called_once_with(
			sort=[('_id', -1)]
		)

	def test_get_next_valid_id_no_documents(self):
		self.mock_chapters.find_one.return_value = None
		result = self.storage.get_next_valid_id('test_db', 'project_db')
		self.assertEqual(result, 1)

	def test_find_chapters_by_lesson(self):
		mock_chapters = [
			{
				"_id": 1,
				"lesson_id": 1,
				"title": "Test Chapter 1",
				"unlock_type": "none",
				"unlock_id": 0,
				"unlocker_id": 0,
				"is_last_in_lesson": False,
				"blocks": []
			}
		]
		mock_find = MagicMock()
		mock_sort = MagicMock()
		mock_sort.__iter__ = lambda _: iter(mock_chapters)
		mock_find.sort.return_value = mock_sort
		self.mock_chapters.find.return_value = mock_find

		result = self.storage.find_chapters('test_db', 'project_db', {"lesson_id": 1})
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0].lesson_id, 1)
		self.mock_chapters.find.assert_called_once_with({"lesson_id": 1})
		mock_find.sort.assert_called_once_with('_id')

class TestChapterDataCollection(TestCase):
	def test_from_dict(self):
		mock_data = [
			{
				"_id": 1,
				"lesson_id": 1,
				"title": "Test Chapter 1",
				"unlock_type": "none",
				"unlock_id": 0,
				"unlocker_id": 0,
				"is_last_in_lesson": False,
				"blocks": []
			}
		]
		result = ChapterDataCollection.from_dict(mock_data)
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0].id, 1)
		self.assertEqual(result[0].title, "Test Chapter 1")
