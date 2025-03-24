from unittest import TestCase
from unittest.mock import MagicMock
from domain.data.blockly.BlocklyData import BlocklyData
from domain.data.blockly.BlocklyStorage import BlocklyStorage
from domain.data.blockly.BlocklyDataCollection import BlocklyDataCollection

class TestBlocklyStorage(TestCase):
	def setUp(self):
		self.mock_db = MagicMock()
		self.storage = BlocklyStorage()
		self.storage.database = {'test_db': self.mock_db}
		self.test_blockly = BlocklyData(
			id=1,
			title="Test Blockly",
			task_description="Test Description",
			expected_task="Expected Task",
			expected_result="Expected Result",
			toolbox={"blocks": []}
		)

	def test_get_blockly(self):
		mock_blockly = {
			"_id": 1,
			"title": "Test Blockly",
			"task_description": "Test Description",
			"expected_task": "Expected Task",
			"expected_result": "Expected Result",
			"toolbox": {"blocks": []}
		}
		self.mock_db.blockly.find_one.return_value = mock_blockly

		result = self.storage.get_blockly('test_db', 1)
		self.assertEqual(result.id, 1)
		self.assertEqual(result.title, "Test Blockly")
		self.mock_db.blockly.find_one.assert_called_once_with({"_id": 1})

	def test_get_blockly_not_found(self):
		self.mock_db.blockly.find_one.return_value = None
		result = self.storage.get_blockly('test_db', 1)
		self.assertIsNone(result)

	def test_find_blockly(self):
		mock_blocklys = [
			{
				"_id": 1,
				"title": "Test Blockly 1",
				"task_description": "Test Description 1",
				"expected_task": "Expected Task 1",
				"expected_result": "Expected Result 1",
				"toolbox": {"blocks": []}
			},
			{
				"_id": 2,
				"title": "Test Blockly 2",
				"task_description": "Test Description 2",
				"expected_task": "Expected Task 2",
				"expected_result": "Expected Result 2",
				"toolbox": {"blocks": []}
			}
		]
		mock_find = MagicMock()
		mock_sort = MagicMock()
		mock_sort.__iter__ = lambda _: iter(mock_blocklys)
		mock_find.sort.return_value = mock_sort
		self.mock_db.blockly.find.return_value = mock_find

		result = self.storage.find_blockly('test_db')
		self.assertEqual(len(result), 2)
		self.assertEqual(result[0].id, 1)
		self.assertEqual(result[1].id, 2)
		self.mock_db.blockly.find.assert_called_once()
		mock_find.sort.assert_called_once_with('_id')

	def test_create_blockly(self):
		self.storage.create_blockly(self.test_blockly, 'test_db')
		self.mock_db.blockly.insert_one.assert_called_once()

	def test_delete_blockly(self):
		self.storage.delete_blockly('test_db', 1)
		self.mock_db.blockly.delete_one.assert_called_once_with({"_id": 1})

	def test_update_blockly(self):
		self.storage.update_blockly(self.test_blockly, 'test_db')
		self.mock_db.blockly.update_one.assert_called_once()

	def test_get_next_valid_id(self):
		mock_document = {"_id": 5}
		self.mock_db.blockly.find_one.return_value = mock_document
		result = self.storage.get_next_valid_id('test_db')
		self.assertEqual(result, 6)

	def test_get_next_valid_id_no_documents(self):
		self.mock_db.blockly.find_one.return_value = None
		result = self.storage.get_next_valid_id('test_db')
		self.assertEqual(result, 1)

class TestBlocklyDataCollection(TestCase):
	def test_from_dict(self):
		mock_data = [
			{
				"_id": 1,
				"title": "Test Blockly 1",
				"task_description": "Test Description 1",
				"expected_task": "Expected Task 1",
				"expected_result": "Expected Result 1",
				"toolbox": {"blocks": []}
			}
		]
		result = BlocklyDataCollection.from_dict(mock_data)
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0].id, 1)
		self.assertEqual(result[0].title, "Test Blockly 1")
