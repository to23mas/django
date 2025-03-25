from django.test import TestCase
from domain.data.lessons.LessonStorage import LessonStorage
from domain.data.lessons.LessonData import LessonData

class TestLessonStorageIntegration(TestCase):
    def setUp(self):
        self.storage = LessonStorage()
        self.test_lesson = LessonData(
            id=999,
            title="Integration Test Lesson",
            to=[1, 2, 3]
        )
        self.test_db = "test_integration_db"
        self.test_project_db = "test_project_db"
        
    def tearDown(self):
        try:
            self.storage.delete_lesson(self.test_db, self.test_project_db, self.test_lesson.id)
        except:
            pass

    def test_create_and_get_lesson(self):
        self.storage.create_lesson(self.test_lesson, self.test_db, self.test_project_db)
        retrieved = self.storage.get_lesson(self.test_lesson.id, self.test_db, self.test_project_db)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.test_lesson.id)
        self.assertEqual(retrieved.title, self.test_lesson.title)
        self.assertEqual(retrieved.to, self.test_lesson.to)

    def test_update_lesson(self):
        self.storage.create_lesson(self.test_lesson, self.test_db, self.test_project_db)
        updated = LessonData(
            id=self.test_lesson.id,
            title="Updated Lesson",
            to=[4, 5, 6]
        )
        self.storage.update_lesson(updated, self.test_db, self.test_project_db)
        retrieved = self.storage.get_lesson(self.test_lesson.id, self.test_db, self.test_project_db)
        self.assertEqual(retrieved.title, "Updated Lesson")
        self.assertEqual(retrieved.to, [4, 5, 6])

    def test_delete_lesson(self):
        self.storage.create_lesson(self.test_lesson, self.test_db, self.test_project_db)
        self.storage.delete_lesson(self.test_db, self.test_project_db, self.test_lesson.id)
        retrieved = self.storage.get_lesson(self.test_lesson.id, self.test_db, self.test_project_db)
        self.assertIsNone(retrieved)

    def test_find_lessons(self):
        self.storage.create_lesson(self.test_lesson, self.test_db, self.test_project_db)
        second_lesson = LessonData(
            id=1000,
            title="Second Lesson",
            to=[7, 8, 9]
        )
        self.storage.create_lesson(second_lesson, self.test_db, self.test_project_db)
        try:
            lessons = self.storage.find_lessons(self.test_db, self.test_project_db)
            self.assertGreaterEqual(len(lessons), 2)
            lesson_ids = [l.id for l in lessons]
            self.assertIn(self.test_lesson.id, lesson_ids)
            self.assertIn(second_lesson.id, lesson_ids)
            self.storage.delete_lesson(self.test_db, self.test_project_db, second_lesson.id)
        except:
            self.storage.delete_lesson(self.test_db, self.test_project_db, second_lesson.id)
            raise

    def test_find_lessons_by_course(self):
        self.storage.create_lesson(self.test_lesson, self.test_db, self.test_project_db)
        lessons = self.storage.find_lessons_by_course(self.test_db, self.test_project_db)
        self.assertGreaterEqual(len(lessons), 1)
        self.assertIn(self.test_lesson.id, [l.id for l in lessons])

    def test_get_next_valid_id(self):
        next_id = self.storage.get_next_valid_id(self.test_db, self.test_project_db)
        self.assertIsInstance(next_id, int)
        self.assertGreater(next_id, 0)
        self.storage.create_lesson(self.test_lesson, self.test_db, self.test_project_db)
        new_next_id = self.storage.get_next_valid_id(self.test_db, self.test_project_db)
        self.assertGreater(new_next_id, next_id) 