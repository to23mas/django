"""storage for lessons"""
from typing import Dict, List

from domain.Mongo import MongoStorage
from domain.data.courses.CourseData import CourseData
from domain.data.courses.CourseDataCollection import CourseDataCollection
from domain.data.courses.CourseDataSerializer import CourseDataSerializer
from domain.data.courses.exception.UniqueDatabaseException import UniqueDatabaseException


def find_courses() -> List[CourseData] | None:
	courses = MongoStorage().database.courses.find().sort('order')

	match courses:
		case None: return courses
		case _: return CourseDataCollection.from_array(courses)


def get_course(filter_: Dict = {}) -> CourseData | None: #pylint: disable=W0102
	course = MongoStorage().database.courses.find_one(filter_)

	match course:
		case None: return course
		case _: return CourseDataSerializer.from_dict(course)


def get_course_by_id(id_: str) -> CourseData | None:
	course = MongoStorage().database.courses.find_one({"_id": int(id_)})

	match course:
		case None: return course
		case _: return CourseDataSerializer.from_dict(course)


def create_course(course_data: CourseData) -> None:
	course = get_course({'database': course_data.database})
	match course:
		case None: MongoStorage().database.courses.insert_one(CourseDataSerializer.to_dict(course_data))
		case _: raise UniqueDatabaseException


def update_course(course_data: CourseData) -> None:
	MongoStorage().database.courses.update_one(
		{'_id': course_data.id},
		{'$set': CourseDataSerializer.to_dict(course_data)}
	)


def delete_course(course_id: str) -> None:
	MongoStorage().database.courses.delete_one({'_id': int(course_id)})


def get_next_valid_id() -> int:
	document = MongoStorage().database.courses.find_one(sort=[('_id', -1)])
	match document:
		case None: return 1
		case _: return document['_id'] + 1
