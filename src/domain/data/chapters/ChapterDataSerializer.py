from typing import Dict, List

from bson.objectid import ObjectId
from domain.data.chapters.ChapterData import ChapterData
from domain.data.chapters.tableDefinition.TableDefinitions import ChaptersTable


class ChapterDataSerializer:

	@staticmethod
	def to_dict(chapter_data: ChapterData) -> Dict[str, str | ObjectId | int | Dict | None]:
		return {
			'_id': ObjectId(chapter_data.id),
			'no': chapter_data.no,
			'title': chapter_data.title,
			'project': chapter_data.project,
			'lesson': chapter_data.lesson,
			'unlock_type': chapter_data.unlock_type,
			'unlock_no': chapter_data.unlock_no,
			'blocks': chapter_data.blocks,
		}


	@staticmethod
	def from_dict(chapter_data: dict) -> ChapterData:
		return ChapterData(
			id=chapter_data[ChaptersTable.ID.value],
			no=chapter_data[ChaptersTable.NO.value],
			title=chapter_data[ChaptersTable.TITLE.value],
			project=chapter_data[ChaptersTable.PROJECT.value],
			lesson=chapter_data[ChaptersTable.LESSON.value],
			unlock_type=chapter_data[ChaptersTable.UNLOCK_TYPE.value],
			unlock_no=chapter_data[ChaptersTable.UNLOCK_TYPE.value],
			blocks=chapter_data[ChaptersTable.BLOCKS.value],
		)
