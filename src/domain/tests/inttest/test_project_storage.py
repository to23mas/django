from django.test import TestCase
from domain.data.projects.ProjectStorage import ProjectStorage
from domain.data.projects.ProjectData import ProjectData
from domain.data.projects.exception.UniqueDatabaseException import UniqueDatabaseException

class TestProjectStorageIntegration(TestCase):
    def setUp(self):
        self.storage = ProjectStorage()
        self.test_project = ProjectData(
            id=999,
            title="Integration Test Project",
            description="Test Description",
            database="test_project_db",
            todo=["Task 1", "Task 2"]
        )
        self.test_db = "test_integration_db"
        
    def tearDown(self):
        try:
            self.storage.delete_project(self.test_db, self.test_project.id)
        except:
            pass

    def test_create_and_get_project(self):
        self.storage.create_project(self.test_project, self.test_db)
        retrieved = self.storage.get_project_by_id(self.test_project.id, self.test_db)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, self.test_project.id)
        self.assertEqual(retrieved.title, self.test_project.title)
        self.assertEqual(retrieved.description, self.test_project.description)
        self.assertEqual(retrieved.database, self.test_project.database)
        self.assertEqual(retrieved.todo, self.test_project.todo)

    def test_unique_database_constraint(self):
        self.storage.create_project(self.test_project, self.test_db)
        duplicate_project = ProjectData(
            id=1000,
            title="Duplicate Project",
            description="Test Description",
            database=self.test_project.database,
            todo=["Task 3", "Task 4"]
        )
        with self.assertRaises(UniqueDatabaseException):
            self.storage.create_project(duplicate_project, self.test_db)

    def test_update_project(self):
        self.storage.create_project(self.test_project, self.test_db)
        updated = ProjectData(
            id=self.test_project.id,
            title="Updated Project",
            description="Updated Description",
            database=self.test_project.database,
            todo=["Task 3", "Task 4"]
        )
        self.storage.update_project(updated, self.test_db)
        retrieved = self.storage.get_project_by_id(self.test_project.id, self.test_db)
        self.assertEqual(retrieved.title, "Updated Project")
        self.assertEqual(retrieved.description, "Updated Description")
        self.assertEqual(retrieved.todo, ["Task 3", "Task 4"])

    def test_delete_project(self):
        self.storage.create_project(self.test_project, self.test_db)
        self.storage.delete_project(self.test_db, self.test_project.id)
        retrieved = self.storage.get_project_by_id(self.test_project.id, self.test_db)
        self.assertIsNone(retrieved)

    def test_find_projects(self):
        self.storage.create_project(self.test_project, self.test_db)
        second_project = ProjectData(
            id=1000,
            title="Second Project",
            description="Second Description",
            database="test_project_db_2",
            todo=["Task 3", "Task 4"]
        )
        self.storage.create_project(second_project, self.test_db)
        try:
            projects = self.storage.find_projects(self.test_db)
            self.assertGreaterEqual(len(projects), 2)
            project_ids = [p.id for p in projects]
            self.assertIn(self.test_project.id, project_ids)
            self.assertIn(second_project.id, project_ids)
            self.storage.delete_project(self.test_db, second_project.id)
        except:
            self.storage.delete_project(self.test_db, second_project.id)
            raise

    def test_find_projects_by_course_and_ids(self):
        self.storage.create_project(self.test_project, self.test_db)
        projects = self.storage.find_projects_by_course_and_ids([self.test_project.id], self.test_db)
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0].id, self.test_project.id)

    def test_get_next_valid_id(self):
        next_id = self.storage.get_next_valid_id(self.test_db)
        self.assertIsInstance(next_id, int)
        self.assertGreater(next_id, 0)
        self.storage.create_project(self.test_project, self.test_db)
        new_next_id = self.storage.get_next_valid_id(self.test_db)
        self.assertGreater(new_next_id, next_id) 