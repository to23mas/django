"""storage for lessons"""
from typing import List
from domain.Mongo import MongoStorage
from domain.data.courses.CourseData import CourseData
from domain.data.courses.CourseDataCollection import CourseDataCollection
from domain.data.courses.CourseDataSerializer import CourseDataSerializer


def find_courses() -> List[CourseData] | None:
	courses = MongoStorage().database.courses.find().sort('order')

	match courses:
		case None: return courses
		case _: return CourseDataCollection.from_array(courses)


def get_course(course_no: str) -> CourseData | None:
	course = MongoStorage().database.courses.find_one({
		"no": int(course_no),
	})

	match course:
		case None: return course
		case _: return CourseDataSerializer.from_array(course)
