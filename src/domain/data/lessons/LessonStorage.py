"""storage for lessons"""
from typing import List
from domain.Mongo import MongoStorage
from domain.data.lessons.LessonData import LessonData
from domain.data.lessons.LessonDataCollection import LessonDataCollection
from domain.data.lessons.LessonDataSerializer import LessonDataSerializer

def get_lesson(lesson_no: str, project_no: str, course: str) -> LessonData | None:
	lesson = MongoStorage().database[course].lessons.find_one({
		"no": int(lesson_no),
		"project": int(project_no),
	})

	match lesson:
		case None: return lesson
		case _: return LessonDataSerializer.from_array(lesson)


def find_lessons(course: str, project_no: str|None=None) -> List[LessonData] | None:
	match project_no:
		case None: lessons = MongoStorage().database[course].lessons.find()
		case _: lessons = MongoStorage().database[course].lessons.find({"project": int(project_no)})

	match lessons:
		case None: return lessons
		case _: return LessonDataCollection.from_array(lessons)
