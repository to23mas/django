"""storage for lessons"""
from typing import List

from bson.objectid import ObjectId
from domain.Mongo import MongoStorage
from domain.data.lessons.LessonData import LessonData
from domain.data.lessons.LessonDataCollection import LessonDataCollection
from domain.data.lessons.LessonDataSerializer import LessonDataSerializer

def get_lesson(lesson_no: str, project_no: str, db: str) -> LessonData | None:
	lesson = MongoStorage().database[db].lessons.find_one({
		"no": int(lesson_no),
		"project": int(project_no),
	})

	match lesson:
		case None: return lesson
		case _: return LessonDataSerializer.from_dict(lesson)


def find_lessons(db: str, project_no: str|None=None) -> List[LessonData] | None:
	match project_no:
		case None: lessons = MongoStorage().database[db].lessons.find()
		case _: lessons = MongoStorage().database[db].lessons.find({"project": int(project_no)})

	match lessons:
		case None: return lessons
		case _: return LessonDataCollection.from_array(lessons)


def exists_lesson(db: str, lesson_no: str) -> bool:
	res = MongoStorage().database[db].lessons.find_one({'no': int(lesson_no)})
	return True if res != None else False


def create_lesson(lesson_data: LessonData, db: str) -> None:
	MongoStorage().database[db].lessons.insert_one(LessonDataSerializer.to_dict(lesson_data))


def delete_lesson(db: str, lesson_id: ObjectId) -> None:
	MongoStorage().database[db].lessons.delete_one({'_id': lesson_id})
