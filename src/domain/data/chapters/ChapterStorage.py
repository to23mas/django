"""storage for lessons"""
from typing import List
from domain.Mongo import MongoStorage
from domain.data.chapters.ChapterData import ChapterData
from domain.data.chapters.ChapterDataCollection import ChapterDataCollection
from domain.data.chapters.ChapterDataSerializer import ChapterDataSerializer


def get_chapter(project_no: str, lesson_no: str, chapter_no: str, db: str) -> ChapterData | None:
	chapter = MongoStorage().database[db].chapters.find_one({
		"no": int(chapter_no),
		"project": int(project_no),
		"lesson": int(lesson_no),
	})

	if chapter == None: return None

	return ChapterDataSerializer.from_array(chapter)

def find_chapter(db: str, lesson_no: str|None=None, project_no: str|None=None) -> List[ChapterData] | None:

	match (project_no, lesson_no):
		case (None, None): query = {}
		case (None, _): query = {"lesson": int(lesson_no)} #type: ignore
		case (_, None): query = {"project": int(project_no)}
		case _: query = {"project": int(project_no), "lesson": int(lesson_no)}

	chapters = MongoStorage().database[db].chapters.find(query)
	match chapters:
		case None: return chapters
		case _: return ChapterDataCollection.from_array(chapters)
