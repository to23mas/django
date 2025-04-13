"""storage for progress"""
from domain.Mongo import MongoStorage
from domain.data.chapters.ChapterStorage import ChapterStorage
from domain.data.courses.CourseStorage import CourseStorage
from domain.data.demos.DemoStorage import DemoStorage
from domain.data.exception.UnexpectedNoneResultException import UnexpectedNoneValueException
from domain.data.lessons.LessonStorage import LessonStorage
from domain.data.progress.enum.ProgressState import ProgressState
from domain.data.projects.ProjectStorage import ProjectStorage
from domain.data.tests.TestStorage import TestStorage
from domain.data.tests.enum.TestState import TestState


class ProgressStorage(MongoStorage):
	def __init__(self):
		super().__init__()


	def get_user_progress_by_course(self, username: str, course: str) -> dict | None:
		return MongoStorage().database[course].progress.find_one({"_id": username})


	def find_users_by_course(self, course: str) -> dict | None:
		return list(MongoStorage().database[course].progress.find({}))


	def get_content_progress(self, db: str, username: str, content: str) -> dict :
		result = MongoStorage().database[db].progress.find(
				{ '_id': username },
				{ f'{content}': 1, '_id': 0 })

		ret_res = list(result)
		if not ret_res:
			return {}
		return ret_res[0][content]


	def enroll_course(self, username: str, db: str) -> bool:
		course = CourseStorage().get_course({'database': db})
		if course is None: return False
		projects = ProjectStorage().find_projects(course.database)
		i = 0
		result_document = {
			"_id": username,
			"projects": {},
			"lessons": {},
			"chapters": {},
			"tests": [],
		}

		for project in projects:
			project_id = str(project.id)

			result_document['projects'][project_id] = ProgressState.OPEN.value if i == 0 else ProgressState.LOCK.value
			result_document['lessons'][project_id] = {}
			result_document['chapters'][project_id] = {}

			lessons = LessonStorage().find_lessons(course.database, project.database)
			j = 0
			if lessons is not None:
				for lesson in lessons:
					result_document['lessons'][project_id][str(lesson.id)] = ProgressState.OPEN.value if j == 0 and i == 0 else ProgressState.LOCK.value
					j += 1

			chapters = ChapterStorage().find_chapters(course.database, project.database)
			k = 0
			if chapters is not None:
				for chapter in chapters:
					result_document['chapters'][project_id][str(chapter.id)] = ProgressState.OPEN.value if i == 0 and k == 0 else ProgressState.LOCK.value
					k += 1
			i += 1

		tests = TestStorage().find_tests(course.database)
		if tests is not None:
			for t in tests:
				result_document['tests'].append({
					"test_id": t.id,
					"attempts": t.attempts,
					"state": "close",
					"score": [],
					"lock_until": '',
				})

		try:
			MongoStorage().database[course.database].progress.insert_one(result_document)
			return True
		except: #pylint: disable=W0702
			return False


	def is_chapter(self, username: str, db: str, chapter_id: int, project_id, target: str) -> bool:
		return MongoStorage().database[db].progress.count_documents({
			'_id': username,
			f'chapters.{project_id}.{chapter_id}': target,
		}) == 1


	def unlock_chapter(self, username: str, db: str, chapter_id: int, project_id: int) -> None:
		if (self.is_chapter(username, db, chapter_id, project_id, 'lock')):
			MongoStorage().database[db].progress.update_one(
				{'_id': username},
				{'$set': {f'chapters.{project_id}.{chapter_id}': 'open'}}
			)


	def finish_chapter(self, username: str, db: str, chapter_id: int, project_id: int) -> None:
		if (self.is_chapter(username, db, chapter_id, project_id, 'open')):
			MongoStorage().database[db].progress.update_one(
				{'_id': username},
				{'$set': { f'chapters.{project_id}.{chapter_id}': 'done' }}
			)


	def find_tests_progress(self, db: str, username: str) -> dict | None:
		"""return user's all tests progress"""
		result = MongoStorage().database[db].progress.find_one({'_id': username}, {'tests': 1})
		if result is None: return None
		return result['tests']


	def find_demos_progress(self, db: str, username: str) -> dict | None:
		"""return user's all tests progress"""
		result = MongoStorage().database[db].progress.find_one({'_id': username}, {'demos': 1})
		if result is None: return None
		return result['demos']


	def find_available_tests(self, course: str, username: str) -> list | None:
		"""return nos of displayable tests (all except closed) tests"""
		all_tests = self.find_tests_progress(course, username)
		if all_tests is None: return None

		available_tests_ids = []
		for test in all_tests:
			if not test['state'] == TestState.CLOSE.value:
				available_tests_ids.append(test['test_id'])

		return available_tests_ids


	def find_available_demos(self, course: str, username: str) -> list[int] | None:
		user_progress = self.get_user_progress_by_course(username, course)
		if user_progress is None: return None

		available_demos_ids = []
		for project_id, project_state in user_progress['projects'].items():
			if (project_state != ProgressState.LOCK.value):
				available_demos_ids.append(int(project_id))

		return available_demos_ids


	def get_project_state(self, course: str, username: str, project_id: int) -> str :
		result = MongoStorage().database[course].progress.find_one(
				{"_id": username },{ f"projects.{project_id}": 1, "_id": 0 }
				)
		if result is None: raise UnexpectedNoneValueException

		return result['projects'][str(project_id)]


	def get_chapter_state(self, db: str, username: str, chapter_id: int, project_id: int) -> str :
		result = MongoStorage().database[db].progress.find_one(
			{"_id": username },
			{ f"chapters.{project_id}.{chapter_id}": 1, "_id": 0 }
		)
		if result is None: raise UnexpectedNoneValueException


		return result['chapters'][str(project_id)][str(chapter_id)]


	def get_lesson_state(self, db: str, username: str, lesson_id: int) -> str :
		result = MongoStorage().database[db].progress.find_one(
			{"_id": username },{ f"lessons.{lesson_id}": 1, "_id": 0 }
		)
		if result is None: raise UnexpectedNoneValueException

		return result['lessons'][str(lesson_id)]


	def is_chapter_done(self, username: str, db: str, chapter_id: int, project_id: int) -> bool:
		return MongoStorage().database[db].progress.count_documents({
			'_id': username,
			f'chapters.{project_id}.{chapter_id}': 'done'
		}) == 1


	def is_chapter_open_or_done(self, username: str, db: str, chapter_id: int, project_id: int) -> bool:
		return MongoStorage().database[db].progress.count_documents({
			'_id': username,
			'$or': [
				{f'chapters.{project_id}.{chapter_id}': 'done'},
				{f'chapters.{project_id}.{chapter_id}': 'open'},
			]
		}) == 1

	def is_chapter_open(self, username: str, db: str, project_id: int, lesson_id: int, chapter_id: int) -> bool:
		return MongoStorage().database[db].progress.count_documents({
			'_id': username,
			f'projects.{project_id}': 'open',
			f'lessons.{project_id}.{lesson_id}': 'open',
			f'chapters.{project_id}.{chapter_id}': 'open',
		}) == 1


	def is_lesson(self, username: str, db: str, lesson_id: int, project_id: int, target: str) -> bool:
		return MongoStorage().database[db].progress.count_documents({
			'_id': username,
			f'lessons.{project_id}.{lesson_id}': target,
		}) == 1


	def is_project(self, username: str, db: str, project_id: int, target: str) -> bool:
		return MongoStorage().database[db].progress.count_documents({
			'_id': username,
			f'projects.{project_id}': target,
		}) == 1


	def unlock_lesson(self, username: str, db: str, lesson_id: int, project_id: int) -> None:
		if (self.is_lesson(username, db, lesson_id, project_id, 'lock')):
			MongoStorage().database[db].progress.update_one(
				{'_id': username},
				{'$set': {f'lessons.{project_id}.{lesson_id}': 'open'}}
			)


	def finish_lesson(self, username: str, db: str, lesson_id: int, project_id: int) -> None:
		if (self.is_lesson(username, db, lesson_id, project_id, 'open')):
			MongoStorage().database[db].progress.update_one(
				{'_id': username},
				{'$set': {f'lessons.{project_id}.{lesson_id}': 'done'}}
			)


	def finish_project(self, db: str, username: str, project_id: int) -> None:
		if (self.is_project(username, db, project_id, 'open')):
			MongoStorage().database[db].progress.update_one(
				{'_id': username}, {'$set': {f'projects.{project_id}': 'done'}}
			)


	def unlock_project(self, db: str, username: str, project_id: int) -> None:
		if (self.is_project(username, db, project_id, 'lock')):
			MongoStorage().database[db].progress.update_one(
				{'_id': username}, {'$set': {f'projects.{project_id}': 'open'}}
			)

