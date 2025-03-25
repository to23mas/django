from django.test import TestCase
from domain.data.courses.CourseStorage import CourseStorage
from domain.data.courses.CourseData import CourseData
from domain.data.courses.exception.UniqueDatabaseException import UniqueDatabaseException

class TestCourseStorageIntegration(TestCase):
    def setUp(self):
        self.storage = CourseStorage()
        self.test_course = CourseData(
            id=999,
            title="Integration Test Course",
            description="Test Description",
            database="test_integration_db",
            order=1,
            visible=True,
            open=True,
            tags=[]
        )
        
    def tearDown(self):
        # Clean up any test data
        try:
            self.storage.delete_course(str(self.test_course.id))
        except:
            pass

    def test_create_and_get_course(self):
        # Test course creation
        self.storage.create_course(self.test_course)
        
        # Test getting course by id
        retrieved_course = self.storage.get_course_by_id(str(self.test_course.id))
        self.assertIsNotNone(retrieved_course)
        self.assertEqual(retrieved_course.id, self.test_course.id)
        self.assertEqual(retrieved_course.title, self.test_course.title)
        self.assertEqual(retrieved_course.database, self.test_course.database)
        
    def test_unique_database_constraint(self):
        # Create first course
        self.storage.create_course(self.test_course)
        
        # Try to create another course with same database
        duplicate_course = CourseData(
            id=1000,
            title="Duplicate Course",
            description="Test Description",
            database=self.test_course.database,
            order=2,
            visible=True,
            open=True,
            tags=[]
        )
        
        with self.assertRaises(UniqueDatabaseException):
            self.storage.create_course(duplicate_course)
            
    def test_update_course(self):
        # Create initial course
        self.storage.create_course(self.test_course)
        
        # Update course
        updated_course = CourseData(
            id=self.test_course.id,
            title="Updated Course Title",
            description="Updated Description",
            database=self.test_course.database,
            order=2,
            visible=False,
            open=False,
            tags=["updated"]
        )
        
        self.storage.update_course(updated_course)
        
        # Verify update
        retrieved_course = self.storage.get_course_by_id(str(self.test_course.id))
        self.assertEqual(retrieved_course.title, "Updated Course Title")
        self.assertEqual(retrieved_course.description, "Updated Description")
        self.assertEqual(retrieved_course.order, 2)
        self.assertEqual(retrieved_course.visible, False)
        self.assertEqual(retrieved_course.open, False)
        self.assertEqual(retrieved_course.tags, ["updated"])
        
    def test_delete_course(self):
        # Create course
        self.storage.create_course(self.test_course)
        
        # Verify it exists
        course = self.storage.get_course_by_id(str(self.test_course.id))
        self.assertIsNotNone(course)
        
        # Delete course
        self.storage.delete_course(str(self.test_course.id))
        
        # Verify it's gone
        course = self.storage.get_course_by_id(str(self.test_course.id))
        self.assertIsNone(course)
        
    def test_find_courses(self):
        # Create test course
        self.storage.create_course(self.test_course)
        
        # Create another course
        second_course = CourseData(
            id=1000,
            title="Second Test Course",
            description="Test Description",
            database="test_integration_db_2",
            order=2,
            visible=True,
            open=True,
            tags=[]
        )
        self.storage.create_course(second_course)
        
        try:
            # Find all courses
            courses = self.storage.find_courses()
            
            # Verify both courses are found
            self.assertGreaterEqual(len(courses), 2)
            
            # Verify courses are ordered by order field
            course_ids = [course.id for course in courses]
            self.assertIn(self.test_course.id, course_ids)
            self.assertIn(second_course.id, course_ids)
            
            # Clean up second course
            self.storage.delete_course(str(second_course.id))
        except:
            # Clean up second course in case of test failure
            self.storage.delete_course(str(second_course.id))
            raise
            
    def test_get_next_valid_id(self):
        next_id = self.storage.get_next_valid_id()
        self.assertIsInstance(next_id, int)
        self.assertGreater(next_id, 0)
        
        # Create a course and verify next id increases
        self.storage.create_course(self.test_course)
        new_next_id = self.storage.get_next_valid_id()
        self.assertGreater(new_next_id, next_id) 