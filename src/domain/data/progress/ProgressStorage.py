"""storage for progress"""
from domain.Mongo import MongoStorage
from domain.data.chapters.ChapterStorage import find_chapters
from domain.data.courses.CourseStorage import get_course
from domain.data.demos.DemoStorage import find_demos
from domain.data.exception.UnexpectedNoneResultException import UnexpectedNoneValueException
from domain.data.lessons.LessonStorage import find_lessons
from domain.data.progress.enum.ProgressState import ProgressState
from domain.data.projects.ProjectStorage import find_projects
from domain.data.tests.TestStorage import find_tests
from domain.data.tests.enum.TestState import TestState


def get_user_progress_by_course(username: str, course: str) -> dict | None:
	return MongoStorage().database[course].progress.find_one({"_id": username})

def get_content_progress(db: str, username: str, content: str) -> dict :
	result = MongoStorage().database[db].progress.find(
		{ '_id': username },
		{ f'{content}': 1, '_id': 0 })

	ret_res = list(result)
	if ret_res == []:
		return {}
	return ret_res[0][content]


def enroll_course(username: str, db: str) -> bool:
	course = get_course({'database': db})
	if course == None: return False
	result_document = {
		"_id": username,
		"projects": {},
		"lessons": {},
		"chapters": {},
		"demos": {},
		"tests": [],
	}

	projects = find_projects(course.database)
	i = 0
	for project in projects:
		result_document['projects'][str(project.id)] = ProgressState.OPEN.value if i == 0 else ProgressState.LOCK.value
		lessons = find_lessons(course.database, project.database)
		j = 0
		if lessons != None:
			for lesson in lessons:
				result_document['lessons'][str(lesson.id)] = ProgressState.OPEN.value if j == 0 and i == 0 else ProgressState.LOCK.value
				j += 1

		chapters = find_chapters(course.database, project.database)
		k = 0
		if chapters != None:
			for chapter in chapters:
				result_document['chapters'][str(chapter.id)] = ProgressState.OPEN.value if i == 0 and k == 0 else ProgressState.LOCK.value
				k += 1
		i += 1

	tests = find_tests(course.database)
	if tests != None:
		for t in tests:
			result_document['tests'].append({
				"test_id": t.id,
				"attempts": t.attempts,
				"state": "close",
				"score": [],
				"lock_until": '',
			})

	demos = find_demos(course.database)
	demo_idx = 0
	if demos != None:
		for demo in demos:
			result_document['demos'][str(demo.id)] = ProgressState.OPEN.value if demo_idx == 0 else ProgressState.LOCK.value
			demo_idx += 1

	try:
		MongoStorage().database[course.database].progress.insert_one(result_document)
		return True
	except:
		return False


def is_chapter(username: str, db: str, chapter_id: int, target: str) -> bool:
	return MongoStorage().database[db].progress.count_documents({
		'_id': username,
		f'chapters.{chapter_id}': target,
	}) == 1


def unlock_chapter(username: str, db: str, chapter_id: int) -> None:
	if (is_chapter(username, db, chapter_id, 'lock')):
		MongoStorage().database[db].progress.update_one(
			{'_id': username},
			{'$set': {f'chapters.{chapter_id}': 'open'}})


def finish_chapter(username: str, db: str, chapter_id: int) -> None:
	if (is_chapter(username, db, chapter_id, 'open')):
		MongoStorage().database[db].progress.update_one(
			{'_id': username},
			{'$set': { f'chapters.{chapter_id}': 'done' }})


def find_tests_progress(db: str, username: str) -> dict | None:
	"""return user's all tests progress"""
	result = MongoStorage().database[db].progress.find_one({'_id': username}, {'tests': 1})
	if result == None: return None
	return result['tests']


def find_demos_progress(db: str, username: str) -> dict | None:
	"""return user's all tests progress"""
	result = MongoStorage().database[db].progress.find_one({'_id': username}, {'demos': 1})
	if result == None: return None
	return result['demos']


def find_available_tests(course: str, username: str) -> list | None:
	"""return nos of displayable tests (all except closed) tests"""
	all_tests = find_tests_progress(course, username)
	if all_tests == None: return None

	available_tests_ids = []
	for test in all_tests:
		if not test['state'] == TestState.CLOSE.value:
			available_tests_ids.append(test['test_id'])

	return available_tests_ids


def find_available_demos(course: str, username: str) -> list[int] | None:
	all_demos = find_demos_progress(course, username)
	if all_demos == None: return None

	available_demo_id = []
	for demo_id in all_demos:
		if (all_demos[demo_id] == ProgressState.OPEN.value):
			available_demo_id.append(int(demo_id))

	return available_demo_id


def get_project_state(course: str, username: str, project_id: int) -> str :
	result = MongoStorage().database[course].progress.find_one(
		{"_id": username },{ f"projects.{project_id}": 1, "_id": 0 }
	)
	if result == None: raise UnexpectedNoneValueException

	return result['projects'][str(project_id)]


def get_chapter_state(db: str, username: str, chapter_id: int) -> str :
	result = MongoStorage().database[db].progress.find_one(
		{"_id": username },{ f"chapters.{chapter_id}": 1, "_id": 0 }
	)
	if result == None: raise UnexpectedNoneValueException

	return result['chapters'][str(chapter_id)]


def get_lesson_state(db: str, username: str, lesson_id: int) -> str :
	result = MongoStorage().database[db].progress.find_one(
		{"_id": username },{ f"lessons.{lesson_id}": 1, "_id": 0 }
	)
	if result == None: raise UnexpectedNoneValueException

	return result['lessons'][str(lesson_id)]


def is_chapter_done(username: str, db: str, chapter_id: int) -> bool:
	return MongoStorage().database[db].progress.count_documents(
		{'_id': username, f'chapters.{chapter_id}': 'done'}
	) == 1


def is_chapter_open_or_done(username: str, db: str, chapter_id: int) -> bool:
	return MongoStorage().database[db].progress.count_documents(
		{'_id': username,
		 '$or': [
			{f'chapters.{chapter_id}': 'done'},
			{f'chapters.{chapter_id}': 'open'},
		]}) == 1

def is_chapter_open(username: str, db: str, project_id: int, lesson_id: int, chapter_id: int) -> bool:
	return MongoStorage().database[db].progress.count_documents({
		'_id': username,
		f'projects.{project_id}': 'open',
		f'lessons.{lesson_id}': 'open',
		f'chapters.{chapter_id}': 'open',
	}) == 1


def is_lesson(username: str, db: str, lesson_id: int, target: str) -> bool:
	return MongoStorage().database[db].progress.count_documents({
		'_id': username,
		f'lessons.{lesson_id}': target,
	}) == 1


def is_project(username: str, db: str, project_id: int, target: str) -> bool:
	return MongoStorage().database[db].progress.count_documents({
		'_id': username,
		f'projects.{project_id}': target,
	}) == 1


def unlock_lesson(username: str, db: str, lesson_id: int) -> None:
	if (is_lesson(username, db, lesson_id, 'lock')):
		MongoStorage().database[db].progress.update_one({
			'_id': username
		}, {'$set': {f'lessons.{lesson_id}': 'open'}})


def finish_lesson(username: str, db: str, lesson_id: int) -> None:
	if (is_lesson(username, db, lesson_id, 'open')):
		MongoStorage().database[db].progress.update_one(
			{'_id': username}, {'$set': {f'lessons.{lesson_id}': 'done'}})


def finish_project(db: str, username: str, project_id: int) -> None:
	if (is_project(username, db, project_id, 'open')):
		MongoStorage().database[db].progress.update_one(
			{'_id': username}, {'$set': {f'projects.{project_id}': 'done'}})


def unlock_project(db: str, username: str, project_id: int) -> None:
	if (is_project(username, db, project_id, 'lock')):
		MongoStorage().database[db].progress.update_one(
			{'_id': username}, {'$set': {f'projects.{project_id}': 'open'}})

