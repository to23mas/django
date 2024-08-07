"""storage for lessons"""
from typing import List

from domain.Mongo import MongoStorage
from domain.data.lessons.LessonData import LessonData
from domain.data.lessons.LessonDataCollection import LessonDataCollection
from domain.data.lessons.LessonDataSerializer import LessonDataSerializer

def get_lesson(lesson_id: int, db: str, project_db: str) -> LessonData | None:
	lesson = MongoStorage().database[db].project[project_db].lessons.find_one({
		"_id": lesson_id,
	})

	match lesson:
		case None: return lesson
		case _: return LessonDataSerializer.from_dict(lesson)


def get_lesson_unique_no(lesson_no: str, db: str) -> LessonData | None:
	lesson = MongoStorage().database[db].lessons.find_one({
		"no": int(lesson_no),
	})

	match lesson:
		case None: return lesson
		case _: return LessonDataSerializer.from_dict(lesson)


def find_lessons(db: str, project_db: str) -> List[LessonData] | None:
	lessons = MongoStorage().database[db].project[project_db].lessons.find().sort('_id')
	match lessons:
		case None: return lessons
		case _: return LessonDataCollection.from_dict(lessons)


def find_lessons_by_course(db: str, project_db) -> List[LessonData]:
	lessons = MongoStorage().database[db].project[project_db].lessons.find()
	return LessonDataCollection.from_dict(lessons)


def exists_lesson(db: str, lesson_no: str) -> bool:
	res = MongoStorage().database[db].lessons.find_one({'no': int(lesson_no)})
	return True if res != None else False


def create_lesson(lesson_data: LessonData, db: str, project_db: str) -> None:
	MongoStorage().database[db].project[project_db].lessons.insert_one(
		LessonDataSerializer.to_dict(lesson_data)
	)


def delete_lesson(db: str, project_db: str, lesson_id: int) -> None:
	MongoStorage().database[db].project[project_db].lessons.delete_one({'_id': lesson_id})


def get_next_valid_id(db: str, project_db: str) -> int:
	document = MongoStorage().database[db].project[project_db].lessons.find_one(sort=[('_id', -1)])
	match document:
		case None: return 1
		case _: return document['_id'] + 1


def update_lesson(lesson_data: LessonData, db: str, project_db: str) -> None:
	MongoStorage().database[db].project[project_db].lessons.update_one(
		{'_id': lesson_data.id},
		{'$set': LessonDataSerializer.to_dict(lesson_data)}
	)
