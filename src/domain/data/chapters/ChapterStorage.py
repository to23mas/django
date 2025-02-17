"""storage for lessons"""
from typing import Dict, List
from domain.Mongo import MongoStorage
from domain.data.chapters.ChapterData import ChapterData
from domain.data.chapters.ChapterDataCollection import ChapterDataCollection
from domain.data.chapters.ChapterDataSerializer import ChapterDataSerializer
from domain.data.chapters.tableDefinition.TableDefinitions import ChaptersTable


class ChapterStorage(MongoStorage):
	def __init__(self):
		super().__init__()


	def get_chapter(self, chapter_id: int, lesson_id: int,  db: str, project_db: str) -> ChapterData | None:
		chapter = self.database[db].project[project_db].chapters.find_one({
			ChaptersTable.ID.value: chapter_id,
			ChaptersTable.LESSON_ID.value: lesson_id,
		})
		match chapter:
			case None: return None
			case _: return ChapterDataSerializer.from_dict(chapter)


	def get_chapter_by_id(self, chapter_id: int, db: str, project_db: str) -> ChapterData | None:
		chapter = self.database[db].project[project_db].chapters.find_one({
			ChaptersTable.ID.value: chapter_id,
		})
		match chapter:
			case None: return None
			case _: return ChapterDataSerializer.from_dict(chapter)


	def find_chapters(self, db: str, project_db: str, query: Dict = {}) -> List[ChapterData] | None: #pylint: disable=W0102
		chapters = self.database[db].project[project_db].chapters.find(query).sort(ChaptersTable.ID.value)
		match chapters:
			case None: return chapters
			case _: return ChapterDataCollection.from_dict(chapters)


	def exists_chapter(self, db: str, chapter_id: str, project_id: str, lesson_id: str) -> bool:
		res = self.database[db].chapters.find_one({
			'no': int(chapter_id),
			'project': int(project_id),
			'lesson': int(lesson_id),
		})

		return res is not None


	def update_chapter(self, chapter_data: ChapterData, db: str, project_db: str, original_lesson_id: int) -> None:
		self.database[db].project[project_db].chapters.update_one(
			{
				ChaptersTable.ID.value: chapter_data.id,
				ChaptersTable.LESSON_ID.value: original_lesson_id
			}, {'$set': ChapterDataSerializer.to_dict(chapter_data)}
		)


	def create_chapter(self, chapter_data: ChapterData, db: str, project_db: str) -> None:
		self.database[db].project[project_db].chapters.insert_one(ChapterDataSerializer.to_dict(chapter_data))


	def create_block(self, chapter_data: ChapterData, db: str, project_db: str, block_data: Dict) -> None:
		self.database[db].project[project_db].chapters.update_one({
			ChaptersTable.ID.value: chapter_data.id,
			ChaptersTable.LESSON_ID.value: chapter_data.lesson_id,
			},{'$push': {'blocks': block_data}})


	def update_block(self, chapter_data: ChapterData, db: str, project_db: str, block_id: int, updated_data: Dict) -> None:
		self.database[db].project[project_db].chapters.update_one({
			ChaptersTable.ID.value: chapter_data.id,
			ChaptersTable.LESSON_ID.value: chapter_data.lesson_id,
			'blocks.id': block_id
		}, {
			'$set': {f'blocks.$.{key}': value for key, value in updated_data.items()}
		})

	def get_next_valid_id(self, db: str, project_db: str) -> int:
		document = self.database[db].project[project_db].chapters.find_one(
			sort=[(ChaptersTable.ID.value, -1)]
		)
		match document:
			case None: return 1
			case _: return document[ChaptersTable.ID.value] + 1


	def get_next_valid_block_id(self, db: str, chapter_id: int, lesson_id: int,  project_db: str) -> int:
		pipeline = [
			{'$match': {
				ChaptersTable.ID.value: chapter_id,
				ChaptersTable.LESSON_ID.value: lesson_id}},
			{"$unwind": "$blocks"},
			{"$group": {"_id": None, "max_id": {"$max": "$blocks.id"}}}
		]

		result = list(self.database[db].project[project_db].chapters.aggregate(pipeline))

		if result:
			return result[0]['max_id'] + 1
		return 1


	def delete_chapter(self, db: str, project_db: str, chapter_id: int, lesson_id: int) -> None:
		self.database[db].project[project_db].chapters.delete_one({
			ChaptersTable.ID.value: chapter_id,
			ChaptersTable.LESSON_ID.value: lesson_id
		})


	def delete_block(self, db: str, project_db: str, chapter_id: int, lesson_id: int, block_id: int) -> None:
		self.database[db].project[project_db].chapters.update_one({
				ChaptersTable.ID.value: chapter_id,
				ChaptersTable.LESSON_ID.value: lesson_id
			}, {'$pull': {'blocks': {'id': block_id}}}
		)
