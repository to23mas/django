"""storage for lessons"""
from typing import Dict

from domain.Mongo import MongoStorage
from domain.data.chapters.ChapterDataSerializer import ChapterDataSerializer
from domain.data.chapters.ChapterStorage import create_chapter
from domain.data.courses.CourseDataSerializer import CourseDataSerializer
from domain.data.courses.CourseStorage import create_course, delete_course, get_course, get_course_by_id
from domain.data.lessons.LessonDataSerializer import LessonDataSerializer
from domain.data.lessons.LessonStorage import create_lesson
from domain.data.projects.ProjectDataSerializer import ProjectDataSerializer
from domain.data.projects.ProjectStorage import create_project, find_projects
from domain.data.tests.QuestionDataSerializer import QuestionDataSerializer
from domain.data.tests.TestDataSerializer import TestDataSerializer
from domain.data.tests.TestStorage import create_question, create_test


def upload_from_json(file_data: Dict) -> Exception | None:
	db = MongoStorage()
	with db.client.start_session() as session:
		session.start_transaction()
		try:
			course_data = CourseDataSerializer.from_dict(file_data['course'])
			create_course(course_data)

			for project in file_data['projects']:
				project_data = ProjectDataSerializer.from_dict(project)
				create_project(project_data, course_data.database)
				for lesson in project['lessons']:
					lesson_data = LessonDataSerializer.from_dict(lesson)
					create_lesson(lesson_data, course_data.database, project_data.database)
				for chapter in project['chapters']:
					chapter_data = ChapterDataSerializer.from_dict(chapter)
					create_chapter(chapter_data, course_data.database, project_data.database)

			for test in file_data['tests']:
				test_data = TestDataSerializer.from_dict(test)
				create_test(test_data, course_data.database)
				for question in test['questions']:
					question_data = QuestionDataSerializer.from_dict(question)
					print(question_data)
					create_question(question_data, test_data.id, course_data.database)

			session.commit_transaction()
			return None
		except Exception as e:
			session.abort_transaction()
			return e

def delete_all(course_id: str) -> None:
	db = MongoStorage()
	course = get_course_by_id(course_id)
	if course == None: return

	projects = find_projects(course.database)
	for project in projects:
		db.database[course.database].project[project.database].lessons.delete_many({})
		db.database[course.database].project[project.database].chapters.delete_many({})

	db.database[course.database].projects.delete_many({})
	db.database[course.database].tests.delete_many({})
	db.database.courses.delete_one({'_id': int(course_id)})
