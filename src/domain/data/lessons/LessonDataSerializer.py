from domain.data.lessons.LessonData import LessonData
from domain.data.lessons.tableDefinition.TableDefinitions import LessonsTable


class LessonDataSerializer:

	@staticmethod
	def from_array(lesson_data: dict) -> LessonData:

		return LessonData(
			no=lesson_data[LessonsTable.NO.value],
			title=lesson_data[LessonsTable.TITLE.value],
			project=lesson_data[LessonsTable.PROJECT.value],
			chapters=lesson_data[LessonsTable.CHAPTERS.value],
		)
