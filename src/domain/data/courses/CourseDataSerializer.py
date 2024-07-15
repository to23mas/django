from typing import Dict, List
from domain.data.courses.CourseData import CourseData
from domain.data.table_definitions.TableDefinitions import CourseTable


class CourseDataSerializer:

	@staticmethod
	def to_dict(course_data: CourseData) -> Dict[str, str | int | List[str]]:
		return {
			'id': str(course_data.id),
			'database': course_data.database,
			'order': course_data.order,
			'no': course_data.no,
			'title': course_data.title,
			'visible': course_data.visible,
			'open': course_data.open,
			'description': course_data.description,
			'tags': ', '.join(course_data.tags)
		}


	@staticmethod
	def from_array(course_data: dict) -> CourseData:
		return CourseData(
			id=course_data[CourseTable.ID.value],
			database=course_data[CourseTable.DATABASE.value],
			order=course_data[CourseTable.ORDER.value],
			no=course_data[CourseTable.NO.value],
			title=course_data[CourseTable.TITLE.value],
			visible=course_data[CourseTable.VISIBLE.value],
			open=course_data[CourseTable.OPEN.value],
			description=course_data[CourseTable.DESCRIPTION.value],
			tags=course_data[CourseTable.TAGS.value],
		)
