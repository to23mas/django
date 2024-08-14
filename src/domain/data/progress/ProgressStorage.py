"""storage for progress"""
from domain.Mongo import MongoStorage
from domain.data.chapters.ChapterStorage import find_chapters
from domain.data.content_progress.enum.ContentProgressState import ContentProgressState
from domain.data.courses.CourseStorage import get_course
from domain.data.lessons.LessonStorage import find_lessons
from domain.data.projects.ProjectStorage import find_projects
from domain.data.tests.TestStorage import find_tests
from domain.data.tests.enum.TestState import TestState


def get_user_progress_by_course(username: str, course: str) -> dict | None:
	return MongoStorage().database[course].progress.find_one({"_id": username})


def enroll_course(username: str, db: str) -> bool:
	course = get_course({'database': db})
	if course == None: return False
	result_document = {
		"_id": username,
		"projects": {},
		"lessons": {},
		"chapters": {},
		"tests": [],
	}

	projects = find_projects(course.database)
	i = 0
	for project in projects:
		result_document['projects'][str(project.id)] = ContentProgressState.OPEN.value if i == 0 else ContentProgressState.LOCK.value
		lessons = find_lessons(course.database, project.database)
		j = 0
		if lessons != None:
			for lesson in lessons:
				result_document['lessons'][str(lesson.id)] = ContentProgressState.OPEN.value if j == 0 and i == 0 else ContentProgressState.LOCK.value
				j += 1

		chapters = find_chapters(course.database, project.database)
		k = 0
		if chapters != None:
			for chapter in chapters:
				result_document['chapters'][str(chapter.id)] = ContentProgressState.OPEN.value if i == 0 and k == 0 else ContentProgressState.LOCK.value
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
			})

	try:
		MongoStorage().database[course.database].progress.insert_one(result_document)
		return True
	except:
		return False


def get_lesson_progress(username: str, project_no: int, course: str) -> dict | None:
    ms = MongoStorage()
    return ms.database[course].progress.find_one(
        {"_id": username, f'lessons.{str(project_no)}': {'$exists': True}},
        {'lessons': 1})


def unlock_project(username: str, project_id: int, unlock: bool) -> None:
    """ if not unlock -> complete """
    ms = MongoStorage()

    to_add = 'open' if unlock else 'done'
    to_rem = 'lock' if unlock else 'open'

    ms.database.progress.update_one(
        {
            '_id': username
        },{
            '$push': {f'projects.{to_add}': project_id},
            '$pull': {f'projects.{to_rem}': project_id}
        })


def unlock_lesson(username: str, course: str, project_no: str, lesson_no: str) -> None:
    ms = MongoStorage()

    ms.database[course].progress.update_one(
        {'_id': username},
        {'$push': {f'lessons.{str(project_no)}.open': int(lesson_no)},
         '$pull': {f'lessons.{str(project_no)}.lock': int(lesson_no)}})


def unlock_chapter(username: str, db: str, chapter_id: int) -> None:
	MongoStorage().database[db].progress.update_one(
		{'_id': username},
		{'$set': {f'chapters.{chapter_id}': 'open'}})


def finish_chapter(username: str, db: str, chapter_id: int) -> None:
	MongoStorage().database[db].progress.update_one(
		{'_id': username},
		{'$set': { f'chapters.{chapter_id}': 'done' }})


def find_tests_progress(db: str, username: str) -> dict | None:
	"""return user's all tests progress"""
	result = MongoStorage().database[db].progress.find_one({'_id': username}, {'tests': 1})
	if result == None: return None
	return result['tests']

def get_test_progress(course: str, username: str, test_id: str) -> dict | None:
    """return user's all tests progress"""
    result = MongoStorage().database[course].progress.find_one({'_id': username}, {'tests': 1})
    if result == None: return None
    return result['tests']


def find_available_tests(course: str, username: str) -> list | None:
	"""return nos of displayable tests (all except closed) tests"""
	all_tests = find_tests_progress(course, username)
	if all_tests == None: return None

	available_tests_nos = []
	for test in all_tests:
		if not test['state'] == TestState.CLOSE.value:
			available_tests_nos.append(test['test_id'])

	return available_tests_nos


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

def unlock_lesson(username: str, db: str, lesson_id: int) -> None:
	MongoStorage().database[db].progress.update_one({
		'_id': username
	}, {'$set': {f'lessons.{lesson_id}': 'open'}})


def finish_lesson(username: str, db: str, lesson_id: int) -> None:
    MongoStorage().database[db].progress.update_one(
        {'_id': username}, {'$set': {f'lessons.{lesson_id}': 'done'}})
