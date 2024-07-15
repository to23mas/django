from typing import Dict, List
from domain.data.lessons.LessonData import LessonData
from domain.data.lessons.tableDefinition.TableDefinitions import LessonsTable


class LessonDataSerializer:

	@staticmethod
	def to_dict(lesson_data: LessonData) -> Dict[str, str | int | List[Dict[str, str|int]]]:
		return {
			'id': str(lesson_data.id),
			'no': lesson_data.no,
			'title': lesson_data.title,
			'project': lesson_data.project,
			'chapters': lesson_data.chapters,
		}


	@staticmethod
	def from_array(lesson_data: dict) -> LessonData:
		return LessonData(
			id=lesson_data[LessonsTable.ID.value],
			no=lesson_data[LessonsTable.NO.value],
			title=lesson_data[LessonsTable.TITLE.value],
			project=lesson_data[LessonsTable.PROJECT.value],
			chapters=lesson_data[LessonsTable.CHAPTERS.value],
		)
