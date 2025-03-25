from django.test import TestCase
from domain.data.clis.CliStorage import CliStorage
from domain.data.clis.CliData import CliData

class TestCliStorageIntegration(TestCase):
    def setUp(self):
        self.storage = CliStorage()
        self.test_cli = CliData(
            id=999,
            title="Integration Test CLI",
            task_description="Test Task Description",
            expected_output="Test Expected Output"
        )
        self.test_db = "test_integration_db"
        
    def tearDown(self):
        try:
            self.storage.delete_cli(self.test_db, self.test_cli.id)
        except:
            pass

    def test_create_and_get_cli(self):
        self.storage.create_cli(self.test_cli, self.test_db)
        retrieved = self.storage.get_cli(self.test_db, self.test_cli.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.test_cli.id)
        self.assertEqual(retrieved.title, self.test_cli.title)
        self.assertEqual(retrieved.task_description, self.test_cli.task_description)
        self.assertEqual(retrieved.expected_output, self.test_cli.expected_output)

    def test_update_cli(self):
        self.storage.create_cli(self.test_cli, self.test_db)
        updated = CliData(
            id=self.test_cli.id,
            title="Updated CLI",
            task_description="Updated Description",
            expected_output="Updated Output"
        )
        self.storage.update_cli(updated, self.test_db)
        retrieved = self.storage.get_cli(self.test_db, self.test_cli.id)
        self.assertEqual(retrieved.title, "Updated CLI")
        self.assertEqual(retrieved.task_description, "Updated Description")
        self.assertEqual(retrieved.expected_output, "Updated Output")

    def test_delete_cli(self):
        self.storage.create_cli(self.test_cli, self.test_db)
        self.storage.delete_cli(self.test_db, self.test_cli.id)
        retrieved = self.storage.get_cli(self.test_db, self.test_cli.id)
        self.assertIsNone(retrieved)

    def test_find_clis(self):
        self.storage.create_cli(self.test_cli, self.test_db)
        second_cli = CliData(
            id=1000,
            title="Second CLI",
            task_description="Second Description",
            expected_output="Second Output"
        )
        self.storage.create_cli(second_cli, self.test_db)
        try:
            clis = self.storage.find_cli(self.test_db)
            self.assertGreaterEqual(len(clis), 2)
            cli_ids = [c.id for c in clis]
            self.assertIn(self.test_cli.id, cli_ids)
            self.assertIn(second_cli.id, cli_ids)
            self.storage.delete_cli(self.test_db, second_cli.id)
        except:
            self.storage.delete_cli(self.test_db, second_cli.id)
            raise

    def test_get_next_valid_id(self):
        next_id = self.storage.get_next_valid_id(self.test_db)
        self.assertIsInstance(next_id, int)
        self.assertGreater(next_id, 0)
        self.storage.create_cli(self.test_cli, self.test_db)
        new_next_id = self.storage.get_next_valid_id(self.test_db)
        self.assertGreater(new_next_id, next_id) 