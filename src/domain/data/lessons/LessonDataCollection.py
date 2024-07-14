from typing import List

from pymongo.cursor import Cursor
from domain.data.lessons.LessonData import LessonData
from domain.data.lessons.LessonDataSerializer import LessonDataSerializer


class LessonDataCollection:

	@staticmethod
	def from_array(lessons_data: dict|Cursor) -> List[LessonData]:
		collection = []
		for lesson in lessons_data:
			collection.append(LessonDataSerializer.from_array(lesson))
		return collection

