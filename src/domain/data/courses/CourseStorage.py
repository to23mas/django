"""storage for lessons"""
from typing import Dict, List

from bson.objectid import ObjectId
from domain.Mongo import MongoStorage
from domain.data.courses.CourseData import CourseData
from domain.data.courses.CourseDataCollection import CourseDataCollection
from domain.data.courses.CourseDataSerializer import CourseDataSerializer


def find_courses() -> List[CourseData] | None:
	courses = MongoStorage().database.courses.find().sort('order')

	match courses:
		case None: return courses
		case _: return CourseDataCollection.from_array(courses)


def get_course(smth: str) -> CourseData | None:
	pass


def get_course_query(query: Dict) -> CourseData | None:
	course = MongoStorage().database.courses.find_one(query)

	match course:
		case None: return course
		case _: return CourseDataSerializer.from_dict(course)


def get_course_by_id(id: str) -> CourseData | None:
	course = MongoStorage().database.courses.find_one({"_id": int(id)})

	match course:
		case None: return course
		case _: return CourseDataSerializer.from_dict(course)


def create_course(course_data: CourseData) -> None:
	MongoStorage().database.courses.insert_one(CourseDataSerializer.to_dict(course_data))


def delete_course(course_id: str) -> None:
	MongoStorage().database.courses.delete_one({'_id': int(course_id)})
