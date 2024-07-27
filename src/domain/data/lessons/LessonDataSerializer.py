from typing import Dict, List

from domain.data.lessons.LessonData import LessonData
from domain.data.lessons.tableDefinition.TableDefinitions import LessonsTable


class LessonDataSerializer:

	@staticmethod
	def to_dict(lesson_data: LessonData) -> Dict[str, str | int | List[int]]:
		return {
			'_id': lesson_data.id,
			'title': lesson_data.title,
			'to': lesson_data.to,
		}


	@staticmethod
	def from_dict(lesson_data: dict) -> LessonData:

		return LessonData(
			id=lesson_data[LessonsTable.ID.value],
			title=lesson_data[LessonsTable.TITLE.value],
			to=lesson_data[LessonsTable.TO.value],
		)
