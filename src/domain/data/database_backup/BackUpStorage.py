# pylint: skip-file
"""storage for lessons"""
from typing import Dict

from domain.Mongo import MongoStorage
from domain.data.blockly.BlocklyStorage import BlocklyStorage
from domain.data.chapters.ChapterDataSerializer import ChapterDataSerializer
from domain.data.chapters.ChapterStorage import ChapterStorage

from domain.data.courses.CourseDataSerializer import CourseDataSerializer
from domain.data.courses.CourseStorage import CourseStorage
from domain.data.demos.DemoDataSerializer import DemoDataSerializer
from domain.data.demos.DemoStorage import DemoStorage
from domain.data.lessons.LessonDataSerializer import LessonDataSerializer
from domain.data.lessons.LessonStorage import LessonStorage
from domain.data.projects.ProjectDataSerializer import ProjectDataSerializer
from domain.data.projects.ProjectStorage import ProjectStorage
from domain.data.tests.QuestionDataSerializer import QuestionDataSerializer
from domain.data.tests.TestDataSerializer import TestDataSerializer
from domain.data.blockly.BlocklyDataSerializer import BlocklyDataSerializer
from domain.data.tests.TestStorage import TestStorage


def download_json(course_id: str) -> Dict | None:
	course = CourseStorage().get_course_by_id(course_id)
	if course is None: return None
	json_result = {'course': CourseDataSerializer.to_dict(course)}

	#PROJECTS LESSONS CHAPTERS
	projects = ProjectStorage().find_projects(course.database)
	json_result['projects'] = [] #type: ignore
	for project in projects:
		project_dict = ProjectDataSerializer.to_dict(project)

		lessons = LessonStorage().find_lessons(course.database, project.database)
		if lessons is None:
			json_result['projects'].append(project_dict)
			continue
		project_dict['lessons'] = [LessonDataSerializer.to_dict(lesson) for lesson in lessons] #type: ignore

		chapters = ChapterStorage().find_chapters(course.database, project.database)
		if chapters is None:
			continue
		project_dict['chapters'] = [ChapterDataSerializer.to_dict(chapter) for chapter in chapters] #type: ignore
		json_result['projects'].append(project_dict)

	#TESTS
	tests = TestStorage().find_tests(course.database)
	json_result['tests'] = [] #type: ignore
	if tests is not None:
		for t in tests:
			_, questions = TestStorage().get_test(course.database, t.id)
			test_dict = TestDataSerializer.to_dict(t)
			if questions is not None:
				test_dict['questions'] = [QuestionDataSerializer.to_dict(question) for question in questions] #type: ignore
			json_result['tests'].append(test_dict)

	blocklys = BlocklyStorage().find_blockly(course.database)
	json_result['blockly'] = [] #type: ignore
	if blocklys is not None:
		for b in blocklys:
			b_dict = BlocklyDataSerializer.to_dict(b)
			json_result['blockly'].append(b_dict)

	demos = DemoStorage().find_demos(course.database)
	json_result['demos'] = [] #type: ignore
	if demos is not None:
		for d in demos:
			d_dict = DemoDataSerializer.to_dict(d)
			json_result['demos'].append(d_dict)

	return json_result


def upload_from_json(file_data: Dict) -> Exception | None:
	db = MongoStorage()
	with db.client.start_session() as session:
		session.start_transaction()
		try:
			course_data = CourseDataSerializer.from_dict(file_data['course'])
			CourseStorage().create_course(course_data)

			for project in file_data['projects']:
				project_data = ProjectDataSerializer.from_dict(project)
				ProjectStorage().create_project(project_data, course_data.database)
				for lesson in project['lessons']:
					lesson_data = LessonDataSerializer.from_dict(lesson)
					LessonStorage().create_lesson(lesson_data, course_data.database, project_data.database)
				for chapter in project['chapters']:
					chapter_data = ChapterDataSerializer.from_dict(chapter)
					ChapterStorage().create_chapter(chapter_data, course_data.database, project_data.database)

			for test in file_data['tests']:
				test_data = TestDataSerializer.from_dict(test)
				TestStorage().create_test(test_data, course_data.database)
				for question in test['questions']:
					question_data = QuestionDataSerializer.from_dict(question)
					TestStorage().create_question(question_data, test_data.id, course_data.database)

			for blockly in file_data['blockly']:
				blockly_data = BlocklyDataSerializer.from_dict(blockly)
				BlocklyStorage().create_blockly(blockly_data, course_data.database)

			for demo in file_data['demos']:
				demo_data = DemoDataSerializer.from_dict(demo)
				DemoStorage().create_demo(demo_data, course_data.database)

			session.commit_transaction()
			return None
		except Exception as e:
			session.abort_transaction()
			return e

def delete_all(course_id: str) -> None:
	db = MongoStorage()
	course = CourseStorage().get_course_by_id(course_id)
	if course is None: return

	projects = ProjectStorage().find_projects(course.database)
	for project in projects:
		db.database[course.database].project[project.database].lessons.delete_many({})
		db.database[course.database].project[project.database].chapters.delete_many({})

	db.database[course.database].projects.delete_many({})
	db.database[course.database].tests.delete_many({})
	db.database[course.database].demos.delete_many({})
	db.database.courses.delete_one({'_id': int(course_id)})
