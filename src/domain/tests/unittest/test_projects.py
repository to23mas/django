from unittest import TestCase
from unittest.mock import MagicMock
from domain.data.projects.ProjectData import ProjectData
from domain.data.projects.ProjectStorage import ProjectStorage
from domain.data.projects.ProjectDataCollection import ProjectDataCollection

class TestProjectStorage(TestCase):
	def setUp(self):
		self.mock_db = MagicMock()
		self.storage = ProjectStorage()
		self.storage.database = {'test_db': self.mock_db}
		self.test_project = ProjectData(
			id=1,
			title="Test Project",
			description="Test Description",
			database="test_db",
			todo=["Task 1", "Task 2"]
		)

	def test_get_project(self):
		mock_project = {
			"_id": 1,
			"title": "Test Project",
			"description": "Test Description",
			"database": "test_db",
			"todo": ["Task 1", "Task 2"]
		}
		self.mock_db.projects.find_one.return_value = mock_project

		result = self.storage.get_project('test_db', {"_id": 1})
		self.assertEqual(result.id, 1)
		self.assertEqual(result.title, "Test Project")
		self.mock_db.projects.find_one.assert_called_once_with({"_id": 1})

	def test_get_project_not_found(self):
		self.mock_db.projects.find_one.return_value = None
		result = self.storage.get_project('test_db', {"_id": 1})
		self.assertIsNone(result)

	def test_find_projects(self):
		mock_projects = [
			{
				"_id": 1,
				"title": "Test Project 1",
				"description": "Test Description 1",
				"database": "test_db",
				"todo": ["Task 1", "Task 2"]
			},
			{
				"_id": 2,
				"title": "Test Project 2",
				"description": "Test Description 2",
				"database": "test_db",
				"todo": ["Task 3", "Task 4"]
			}
		]
		mock_find = MagicMock()
		mock_sort = MagicMock()
		mock_sort.__iter__ = lambda _: iter(mock_projects)
		mock_find.sort.return_value = mock_sort
		self.mock_db.projects.find.return_value = mock_find

		result = self.storage.find_projects('test_db')
		self.assertEqual(len(result), 2)
		self.assertEqual(result[0].id, 1)
		self.assertEqual(result[1].id, 2)
		self.mock_db.projects.find.assert_called_once()
		mock_find.sort.assert_called_once_with('_id')

	def test_create_project(self):
		self.mock_db.projects.find_one.return_value = None
		self.storage.create_project(self.test_project, 'test_db')
		self.mock_db.projects.insert_one.assert_called_once()

	def test_delete_project(self):
		self.storage.delete_project('test_db', 1)
		self.mock_db.projects.delete_one.assert_called_once_with({"_id": 1})

	def test_update_project(self):
		self.storage.update_project(self.test_project, 'test_db')
		self.mock_db.projects.update_one.assert_called_once()

	def test_get_next_valid_id(self):
		mock_document = {"_id": 5}
		self.mock_db.projects.find_one.return_value = mock_document
		result = self.storage.get_next_valid_id('test_db')
		self.assertEqual(result, 6)

	def test_get_next_valid_id_no_documents(self):
		self.mock_db.projects.find_one.return_value = None
		result = self.storage.get_next_valid_id('test_db')
		self.assertEqual(result, 1)

class TestProjectDataCollection(TestCase):
	def test_from_dict(self):
		mock_data = [
			{
				"_id": 1,
				"title": "Test Project 1",
				"description": "Test Description 1",
				"database": "test_db",
				"todo": ["Task 1", "Task 2"]
			}
		]
		result = ProjectDataCollection.from_dict(mock_data)
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0].id, 1)
		self.assertEqual(result[0].title, "Test Project 1")
		self.assertEqual(result[0].todo, ["Task 1", "Task 2"])
