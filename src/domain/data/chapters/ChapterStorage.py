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

	return ChapterDataSerializer.from_dict(chapter)

def find_chapter(db: str, project_db: str) -> List[ChapterData] | None:
	chapters = MongoStorage().database[db].project[project_db].chapters.find().sort('_id')
	match chapters:
		case None: return chapters
		case _: return ChapterDataCollection.from_array(chapters)

def exists_chapter(db: str, chapter_id: str, project_id: str, lesson_id: str) -> bool:
	res = MongoStorage().database[db].chapters.find_one({
		'no': int(chapter_id),
		'project': int(project_id),
		'lesson': int(lesson_id),
	})
	return True if res != None else False


def create_chapter(chapter_data: ChapterData, db: str) -> None:
	MongoStorage().database[db].chapters.insert_one(ChapterDataSerializer.to_dict(chapter_data))
