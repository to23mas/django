from typing import List

from pymongo.cursor import Cursor
from domain.data.courses.CourseData import CourseData
from domain.data.courses.CourseDataSerializer import CourseDataSerializer


class CourseDataCollection:

	@staticmethod
	def from_array(course_data: dict|Cursor) -> List[CourseData]:
		collection = []
		for course in course_data:
			collection.append(CourseDataSerializer.from_array(course))
		return collection
