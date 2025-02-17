"""storage for lessons"""
from typing import List

from domain.Mongo import MongoStorage
from domain.data.lessons.LessonData import LessonData
from domain.data.lessons.LessonDataCollection import LessonDataCollection
from domain.data.lessons.LessonDataSerializer import LessonDataSerializer

class LessonStorage(MongoStorage):
	def __init__(self):
		super().__init__()


	def get_lesson(self, lesson_id: int, db: str, project_db: str) -> LessonData | None:
		lesson = self.database[db].project[project_db].lessons.find_one({
			"_id": lesson_id,
		})

		match lesson:
			case None: return lesson
			case _: return LessonDataSerializer.from_dict(lesson)


	def get_lesson_unique_no(self, lesson_no: str, db: str) -> LessonData | None:
		lesson = self.database[db].lessons.find_one({
			"no": int(lesson_no),
		})

		match lesson:
			case None: return lesson
			case _: return LessonDataSerializer.from_dict(lesson)


	def find_lessons(self, db: str, project_db: str) -> List[LessonData] | None:
		lessons = self.database[db].project[project_db].lessons.find().sort('_id')
		match lessons:
			case None: return lessons
			case _: return LessonDataCollection.from_dict(lessons)


	def find_lessons_by_course(self, db: str, project_db) -> List[LessonData]:
		lessons = self.database[db].project[project_db].lessons.find()
		return LessonDataCollection.from_dict(lessons)


	def exists_lesson(self, db: str, lesson_no: str) -> bool:
		res = self.database[db].lessons.find_one({'no': int(lesson_no)})
		return res is not None


	def create_lesson(self, lesson_data: LessonData, db: str, project_db: str) -> None:
		self.database[db].project[project_db].lessons.insert_one(
			LessonDataSerializer.to_dict(lesson_data)
		)


	def delete_lesson(self, db: str, project_db: str, lesson_id: int) -> None:
		self.database[db].project[project_db].lessons.delete_one({'_id': lesson_id})


	def get_next_valid_id(self, db: str, project_db: str) -> int:
		document = self.database[db].project[project_db].lessons.find_one(sort=[('_id', -1)])
		match document:
			case None: return 1
			case _: return document['_id'] + 1


	def update_lesson(self, lesson_data: LessonData, db: str, project_db: str) -> None:
		self.database[db].project[project_db].lessons.update_one(
			{'_id': lesson_data.id},
			{'$set': LessonDataSerializer.to_dict(lesson_data)}
		)
