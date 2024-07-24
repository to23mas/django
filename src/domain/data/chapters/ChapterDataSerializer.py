from typing import Dict

from domain.data.chapters.ChapterData import ChapterData
from domain.data.chapters.tableDefinition.TableDefinitions import ChaptersTable


class ChapterDataSerializer:

	@staticmethod
	def to_dict(chapter_data: ChapterData) -> Dict[str, str | int | Dict | None]:
		return {
			'_id': chapter_data.id,
			'title': chapter_data.title,
			'lesson_id': chapter_data.lesson_id,
			'unlock_type': chapter_data.unlock_type,
			'unlock_id': chapter_data.unlock_id,
			'blocks': chapter_data.blocks,
		}


	@staticmethod
	def from_dict(chapter_data: dict) -> ChapterData:
		print(chapter_data)
		return ChapterData(
			id=chapter_data[ChaptersTable.ID.value],
			title=chapter_data[ChaptersTable.TITLE.value],
			lesson_id=chapter_data[ChaptersTable.LESSON_ID.value],
			unlock_type=chapter_data[ChaptersTable.UNLOCK_TYPE.value],
			unlock_id=chapter_data[ChaptersTable.UNLOCK_ID.value],
			blocks=chapter_data[ChaptersTable.BLOCKS.value],
		)
