from typing import Dict, List

from domain.data.lessons.LessonData import LessonData
from domain.data.lessons.tableDefinition.TableDefinitions import LessonsTable


class LessonDataSerializer:

	@staticmethod
	def to_dict(lesson_data: LessonData) -> Dict[str, str | int | None | List[Dict[str, str|int]]]:
		return {
			'_id': lesson_data.id,
			'title': lesson_data.title,
			'chapters': lesson_data.chapters,
		}


	@staticmethod
	def from_dict(lesson_data: dict) -> LessonData:
		try:
			chapters = lesson_data[LessonsTable.CHAPTERS.value]
		except KeyError:
			chapters = None

		return LessonData(
			id=lesson_data[LessonsTable.ID.value],
			title=lesson_data[LessonsTable.TITLE.value],
			chapters=chapters
		)
