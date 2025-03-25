from django.test import TestCase
from domain.data.blockly.BlocklyStorage import BlocklyStorage
from domain.data.blockly.BlocklyData import BlocklyData

class TestBlocklyStorageIntegration(TestCase):
    def setUp(self):
        self.storage = BlocklyStorage()
        self.test_blockly = BlocklyData(
            id=999,
            title="Integration Test Blockly",
            task_description="Test Task Description",
            expected_task="Test Expected Task",
            expected_result="Test Expected Result",
            toolbox={"test": "toolbox"}
        )
        self.test_db = "test_integration_db"
        
    def tearDown(self):
        try:
            self.storage.delete_blockly(self.test_db, self.test_blockly.id)
        except:
            pass

    def test_create_and_get_blockly(self):
        self.storage.create_blockly(self.test_blockly, self.test_db)
        retrieved = self.storage.get_blockly(self.test_db, self.test_blockly.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.test_blockly.id)
        self.assertEqual(retrieved.title, self.test_blockly.title)
        self.assertEqual(retrieved.task_description, self.test_blockly.task_description)
        self.assertEqual(retrieved.expected_task, self.test_blockly.expected_task)
        self.assertEqual(retrieved.expected_result, self.test_blockly.expected_result)
        self.assertEqual(retrieved.toolbox, self.test_blockly.toolbox)

    def test_update_blockly(self):
        self.storage.create_blockly(self.test_blockly, self.test_db)
        updated = BlocklyData(
            id=self.test_blockly.id,
            title="Updated Blockly",
            task_description="Updated Description",
            expected_task="Updated Task",
            expected_result="Updated Result",
            toolbox={"updated": "toolbox"}
        )
        self.storage.update_blockly(updated, self.test_db)
        retrieved = self.storage.get_blockly(self.test_db, self.test_blockly.id)
        self.assertEqual(retrieved.title, "Updated Blockly")
        self.assertEqual(retrieved.task_description, "Updated Description")
        self.assertEqual(retrieved.expected_task, "Updated Task")
        self.assertEqual(retrieved.expected_result, "Updated Result")
        self.assertEqual(retrieved.toolbox, {"updated": "toolbox"})

    def test_delete_blockly(self):
        self.storage.create_blockly(self.test_blockly, self.test_db)
        self.storage.delete_blockly(self.test_db, self.test_blockly.id)
        retrieved = self.storage.get_blockly(self.test_db, self.test_blockly.id)
        self.assertIsNone(retrieved)

    def test_find_blocklies(self):
        self.storage.create_blockly(self.test_blockly, self.test_db)
        second_blockly = BlocklyData(
            id=1000,
            title="Second Blockly",
            task_description="Second Description",
            expected_task="Second Task",
            expected_result="Second Result",
            toolbox={"second": "toolbox"}
        )
        self.storage.create_blockly(second_blockly, self.test_db)
        try:
            blocklies = self.storage.find_blockly(self.test_db)
            self.assertGreaterEqual(len(blocklies), 2)
            blockly_ids = [b.id for b in blocklies]
            self.assertIn(self.test_blockly.id, blockly_ids)
            self.assertIn(second_blockly.id, blockly_ids)
            self.storage.delete_blockly(self.test_db, second_blockly.id)
        except:
            self.storage.delete_blockly(self.test_db, second_blockly.id)
            raise

    def test_get_next_valid_id(self):
        next_id = self.storage.get_next_valid_id(self.test_db)
        self.assertIsInstance(next_id, int)
        self.assertGreater(next_id, 0)
        self.storage.create_blockly(self.test_blockly, self.test_db)
        new_next_id = self.storage.get_next_valid_id(self.test_db)
        self.assertGreater(new_next_id, next_id) 