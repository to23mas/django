from unittest import TestCase
from unittest.mock import MagicMock
from domain.data.demos.DemoData import DemoData
from domain.data.demos.DemoStorage import DemoStorage
from domain.data.demos.DemoDataCollection import DemoDataCollection

class TestDemoStorage(TestCase):
	def setUp(self):
		self.mock_db = MagicMock()
		self.storage = DemoStorage()
		self.storage.database = {'test_db': self.mock_db}
		self.test_demo = DemoData(
			id=1,
			name="Test Demo",
			url="http://test.com"
		)

	def test_get_demo(self):
		mock_demo = {
			"_id": 1,
			"name": "Test Demo",
			"url": "http://test.com"
		}
		self.mock_db.demos.find_one.return_value = mock_demo

		result = self.storage.get_demo(1, 'test_db')
		self.assertEqual(result.id, 1)
		self.assertEqual(result.name, "Test Demo")
		self.mock_db.demos.find_one.assert_called_once_with({"_id": 1})

	def test_get_demo_not_found(self):
		self.mock_db.demos.find_one.return_value = None
		result = self.storage.get_demo(1, 'test_db')
		self.assertIsNone(result)

	def test_find_demos(self):
		mock_demos = [
			{
				"_id": 1,
				"name": "Test Demo 1",
				"url": "http://test1.com"
			},
			{
				"_id": 2,
				"name": "Test Demo 2",
				"url": "http://test2.com"
			}
		]
		mock_find = MagicMock()
		mock_sort = MagicMock()
		mock_sort.__iter__ = lambda _: iter(mock_demos)
		mock_find.sort.return_value = mock_sort
		self.mock_db.demos.find.return_value = mock_find

		result = self.storage.find_demos('test_db')
		self.assertEqual(len(result), 2)
		self.assertEqual(result[0].id, 1)
		self.assertEqual(result[1].id, 2)
		self.mock_db.demos.find.assert_called_once()
		mock_find.sort.assert_called_once_with('_id')

	def test_create_demo(self):
		self.storage.create_demo(self.test_demo, 'test_db')
		self.mock_db.demos.insert_one.assert_called_once()

	def test_delete_demo(self):
		self.storage.delete_demo('test_db', 1)
		self.mock_db.demos.delete_one.assert_called_once_with({"_id": 1})

	def test_update_demo(self):
		self.storage.update_demo(self.test_demo, 'test_db')
		self.mock_db.demos.update_one.assert_called_once()

	def test_get_next_valid_id(self):
		mock_document = {"_id": 5}
		self.mock_db.demos.find_one.return_value = mock_document
		result = self.storage.get_next_valid_id('test_db')
		self.assertEqual(result, 6)

	def test_get_next_valid_id_no_documents(self):
		self.mock_db.demos.find_one.return_value = None
		result = self.storage.get_next_valid_id('test_db')
		self.assertEqual(result, 1)

class TestDemoDataCollection(TestCase):
	def test_from_dict(self):
		mock_data = [
			{
				"_id": 1,
				"name": "Test Demo 1",
				"url": "http://test1.com"
			}
		]
		result = DemoDataCollection.from_dict(mock_data)
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0].id, 1)
		self.assertEqual(result[0].name, "Test Demo 1")
