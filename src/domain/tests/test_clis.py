from unittest import TestCase
from unittest.mock import MagicMock
from domain.data.clis.CliData import CliData
from domain.data.clis.CliStorage import CliStorage
from domain.data.clis.CliDataCollection import CliDataCollection

class TestCliStorage(TestCase):
	def setUp(self):
		self.mock_db = MagicMock()
		self.storage = CliStorage()
		self.storage.database = {'test_db': self.mock_db}
		self.test_cli = CliData(
			id=1,
			title="Test CLI",
			task_description="Test Description",
			expected_output="Test Output"
		)

	def test_get_cli(self):
		mock_cli = {
			"_id": 1,
			"title": "Test CLI",
			"task_description": "Test Description",
			"expected_output": "Test Output"
		}
		self.mock_db.cli.find_one.return_value = mock_cli

		result = self.storage.get_cli('test_db', 1)
		self.assertEqual(result.id, 1)
		self.assertEqual(result.title, "Test CLI")
		self.mock_db.cli.find_one.assert_called_once_with({"_id": 1})

	def test_get_cli_not_found(self):
		self.mock_db.cli.find_one.return_value = None
		result = self.storage.get_cli('test_db', 1)
		self.assertIsNone(result)

	def test_find_clis(self):
		mock_clis = [
			{
				"_id": 1,
				"title": "Test CLI 1",
				"task_description": "Test Description 1",
				"expected_output": "Test Output 1"
			},
			{
				"_id": 2,
				"title": "Test CLI 2",
				"task_description": "Test Description 2",
				"expected_output": "Test Output 2"
			}
		]
		mock_find = MagicMock()
		mock_sort = MagicMock()
		mock_sort.__iter__ = lambda _: iter(mock_clis)
		mock_find.sort.return_value = mock_sort
		self.mock_db.cli.find.return_value = mock_find

		result = self.storage.find_cli('test_db')
		self.assertEqual(len(result), 2)
		self.assertEqual(result[0].id, 1)
		self.assertEqual(result[1].id, 2)
		self.mock_db.cli.find.assert_called_once()
		mock_find.sort.assert_called_once_with('_id')

	def test_create_cli(self):
		self.storage.create_cli(self.test_cli, 'test_db')
		self.mock_db.cli.insert_one.assert_called_once()

	def test_delete_cli(self):
		self.storage.delete_cli('test_db', 1)
		self.mock_db.cli.delete_one.assert_called_once_with({"_id": 1})

	def test_update_cli(self):
		self.storage.update_cli(self.test_cli, 'test_db')
		self.mock_db.cli.update_one.assert_called_once()

	def test_get_next_valid_id(self):
		mock_document = {"_id": 5}
		self.mock_db.cli.find_one.return_value = mock_document
		result = self.storage.get_next_valid_id('test_db')
		self.assertEqual(result, 6)

	def test_get_next_valid_id_no_documents(self):
		self.mock_db.cli.find_one.return_value = None
		result = self.storage.get_next_valid_id('test_db')
		self.assertEqual(result, 1)

class TestCliDataCollection(TestCase):
	def test_from_dict(self):
		mock_data = [
			{
				"_id": 1,
				"title": "Test CLI 1",
				"task_description": "Test Description 1",
				"expected_output": "Test Output 1"
			}
		]
		result = CliDataCollection.from_dict(mock_data)
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0].id, 1)
		self.assertEqual(result[0].title, "Test CLI 1")
