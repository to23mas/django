from django.test import TestCase
from domain.data.demos.DemoStorage import DemoStorage
from domain.data.demos.DemoData import DemoData

class TestDemoStorageIntegration(TestCase):
    def setUp(self):
        self.storage = DemoStorage()
        self.test_demo = DemoData(
            id=999,
            project_id=1,
            name="Integration Test Demo",
            url="http://test.com"
        )
        self.test_db = "test_integration_db"
        
    def tearDown(self):
        try:
            self.storage.delete_demo(self.test_db, self.test_demo.id)
        except:
            pass

    def test_create_and_get_demo(self):
        self.storage.create_demo(self.test_demo, self.test_db)
        retrieved = self.storage.get_demo(self.test_demo.id, self.test_db)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.test_demo.id)
        self.assertEqual(retrieved.name, self.test_demo.name)
        self.assertEqual(retrieved.url, self.test_demo.url)
        self.assertEqual(retrieved.project_id, self.test_demo.project_id)

    def test_update_demo(self):
        self.storage.create_demo(self.test_demo, self.test_db)
        updated = DemoData(
            id=self.test_demo.id,
            project_id=2,
            name="Updated Demo",
            url="http://updated.com"
        )
        self.storage.update_demo(updated, self.test_db)
        retrieved = self.storage.get_demo(self.test_demo.id, self.test_db)
        self.assertEqual(retrieved.name, "Updated Demo")
        self.assertEqual(retrieved.url, "http://updated.com")
        self.assertEqual(retrieved.project_id, 2)

    def test_delete_demo(self):
        self.storage.create_demo(self.test_demo, self.test_db)
        self.storage.delete_demo(self.test_db, self.test_demo.id)
        retrieved = self.storage.get_demo(self.test_demo.id, self.test_db)
        self.assertIsNone(retrieved)

    def test_find_demos(self):
        self.storage.create_demo(self.test_demo, self.test_db)
        second_demo = DemoData(
            id=1000,
            project_id=2,
            name="Second Demo",
            url="http://second.com"
        )
        self.storage.create_demo(second_demo, self.test_db)
        try:
            demos = self.storage.find_demos(self.test_db)
            self.assertGreaterEqual(len(demos), 2)
            demo_ids = [d.id for d in demos]
            self.assertIn(self.test_demo.id, demo_ids)
            self.assertIn(second_demo.id, demo_ids)
            self.storage.delete_demo(self.test_db, second_demo.id)
        except:
            self.storage.delete_demo(self.test_db, second_demo.id)
            raise

    def test_get_next_valid_id(self):
        next_id = self.storage.get_next_valid_id(self.test_db)
        self.assertIsInstance(next_id, int)
        self.assertGreater(next_id, 0)
        self.storage.create_demo(self.test_demo, self.test_db)
        new_next_id = self.storage.get_next_valid_id(self.test_db)
        self.assertGreater(new_next_id, next_id) 