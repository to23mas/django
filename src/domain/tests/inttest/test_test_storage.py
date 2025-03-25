from django.test import TestCase
from domain.data.tests.TestStorage import TestStorage
from domain.data.tests.TestData import TestData
from domain.data.tests.QuestionData import QuestionData

class TestTestStorageIntegration(TestCase):
    def setUp(self):
        self.storage = TestStorage()
        self.test_test = TestData(
            id=999,
            title="Integration Test Test",
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
            total_points=100,
            current_project=1
        )
        self.test_db = "test_integration_db"
        
    def tearDown(self):
        try:
            self.storage.delete_test(self.test_db, self.test_test.id)
        except:
            pass

    def test_create_and_get_test(self):
        self.storage.create_test(self.test_test, self.test_db)
        retrieved, questions = self.storage.get_test(self.test_db, self.test_test.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.test_test.id)
        self.assertEqual(retrieved.title, self.test_test.title)
        self.assertEqual(retrieved.time, self.test_test.time)
        self.assertEqual(retrieved.description, self.test_test.description)
        self.assertEqual(retrieved.unlock_lesson, self.test_test.unlock_lesson)
        self.assertEqual(retrieved.unlock_chapter, self.test_test.unlock_chapter)
        self.assertEqual(retrieved.unlock_project, self.test_test.unlock_project)
        self.assertEqual(retrieved.finish_project, self.test_test.finish_project)
        self.assertEqual(retrieved.finish_lesson, self.test_test.finish_lesson)
        self.assertEqual(retrieved.finish_chapter, self.test_test.finish_chapter)
        self.assertEqual(retrieved.current_project, self.test_test.current_project)
        self.assertEqual(retrieved.attempts, self.test_test.attempts)
        self.assertEqual(retrieved.success_score, self.test_test.success_score)
        self.assertEqual(retrieved.total_points, 0)  # No questions yet
        self.assertIsNone(questions)

    def test_update_test(self):
        self.storage.create_test(self.test_test, self.test_db)
        updated = TestData(
            id=self.test_test.id,
            title="Updated Test",
            time=60,
            description="Updated Description",
            unlock_lesson=1,
            unlock_chapter=1,
            unlock_project=1,
            finish_project=1,
            finish_lesson=1,
            finish_chapter=1,
            attempts=3,
            success_score=70.0,
            total_points=200,
            current_project=1
        )
        self.storage.update_test(updated, self.test_db)
        retrieved, questions = self.storage.get_test(self.test_db, self.test_test.id)
        self.assertEqual(retrieved.title, "Updated Test")
        self.assertEqual(retrieved.time, 60)
        self.assertEqual(retrieved.description, "Updated Description")
        self.assertEqual(retrieved.unlock_lesson, 1)
        self.assertEqual(retrieved.unlock_chapter, 1)
        self.assertEqual(retrieved.unlock_project, 1)
        self.assertEqual(retrieved.finish_project, 1)
        self.assertEqual(retrieved.finish_lesson, 1)
        self.assertEqual(retrieved.finish_chapter, 1)
        self.assertEqual(retrieved.current_project, 1)
        self.assertEqual(retrieved.attempts, 3)
        self.assertEqual(retrieved.success_score, 70.0)
        self.assertEqual(retrieved.total_points, 0)  # No questions yet
        self.assertIsNone(questions)

    def test_delete_test(self):
        self.storage.create_test(self.test_test, self.test_db)
        self.storage.delete_test(self.test_db, self.test_test.id)
        with self.assertRaises(Exception):
            self.storage.get_test(self.test_db, self.test_test.id)

    def test_find_tests(self):
        self.storage.create_test(self.test_test, self.test_db)
        second_test = TestData(
            id=1000,
            title="Second Test",
            time=60,
            description="Second Description",
            unlock_lesson=1,
            unlock_chapter=1,
            unlock_project=1,
            finish_project=1,
            finish_lesson=1,
            finish_chapter=1,
            attempts=3,
            success_score=70.0,
            total_points=100,
            current_project=1
        )
        self.storage.create_test(second_test, self.test_db)
        try:
            tests = self.storage.find_tests(self.test_db)
            self.assertGreaterEqual(len(tests), 2)
            test_ids = [t.id for t in tests]
            self.assertIn(self.test_test.id, test_ids)
            self.assertIn(second_test.id, test_ids)
            self.storage.delete_test(self.test_db, second_test.id)
        except:
            self.storage.delete_test(self.test_db, second_test.id)
            raise

    def test_find_tests_for_overview(self):
        self.storage.create_test(self.test_test, self.test_db)
        tests = self.storage.find_tests_for_overview(self.test_db, [self.test_test.id])
        self.assertEqual(len(tests), 1)
        self.assertEqual(tests[0].id, self.test_test.id)

    def test_get_next_valid_id(self):
        next_id = self.storage.get_next_valid_id(self.test_db)
        self.assertIsInstance(next_id, int)
        self.assertGreater(next_id, 0)
        self.storage.create_test(self.test_test, self.test_db)
        new_next_id = self.storage.get_next_valid_id(self.test_db)
        self.assertGreater(new_next_id, next_id) 