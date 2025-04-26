from typing import Dict, List

from domain.data.chapters.ChapterData import ChapterData
from domain.data.chapters.tableDefinition.TableDefinitions import ChaptersTable


class ChapterDataSerializer:

	@staticmethod
	def to_dict(chapter_data: ChapterData) -> Dict[str, str | int | List[Dict] | None]:
		return {
			'_id': chapter_data.id,
			'title': chapter_data.title,
			'lesson_id': chapter_data.lesson_id,
			'unlock_type': chapter_data.unlock_type,
			'unlock_id': chapter_data.unlock_id,
			'unlocker_id': chapter_data.unlocker_id,
			'is_last_in_lesson': chapter_data.is_last_in_lesson,
			'blocks': chapter_data.blocks,
		}


	@staticmethod
	def from_dict(chapter_data: dict, ch_with_blocks: ChapterData|None = None) -> ChapterData:
		try:
			blocks = chapter_data[ChaptersTable.BLOCKS.value]
		except: #pylint: disable=W0702
			blocks = []

		if ch_with_blocks is not None:
			blocks = ch_with_blocks.blocks

		blocks = sorted(blocks, key=lambda x: x.get('order', 0))

		return ChapterData(
			id=chapter_data[ChaptersTable.ID.value],
			title=chapter_data[ChaptersTable.TITLE.value],
			lesson_id=chapter_data[ChaptersTable.LESSON_ID.value],
			unlock_type=chapter_data[ChaptersTable.UNLOCK_TYPE.value],
			unlock_id=int(chapter_data[ChaptersTable.UNLOCK_ID.value]),
			unlocker_id=chapter_data[ChaptersTable.UNLOCKER_ID.value],
			is_last_in_lesson=bool(chapter_data[ChaptersTable.IS_LAST_IN_LESSON.value]),
			blocks=blocks
		)
