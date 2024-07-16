from typing import Dict, List
from domain.data.chapters.ChapterData import ChapterData
from domain.data.chapters.tableDefinition.TableDefinitions import ChaptersTable


class ChapterDataSerializer:

	@staticmethod
	def to_dict(chapter_data: ChapterData) -> Dict[str, str | int | Dict | None]:
		return {
			'no': chapter_data.no,
			'title': chapter_data.title,
			'project': chapter_data.project,
			'lesson': chapter_data.lesson,
			'unlock_type': chapter_data.unlocks.get('type'),
			'unlock_no': chapter_data.unlocks.get('no'),
			'blocks': chapter_data.blocks,
		}


	@staticmethod
	def from_array(chapter_data: dict) -> ChapterData:
		return ChapterData(
			no=chapter_data[ChaptersTable.NO.value],
			title=chapter_data[ChaptersTable.TITLE.value],
			project=chapter_data[ChaptersTable.PROJECT.value],
			lesson=chapter_data[ChaptersTable.LESSON.value],
			unlocks=chapter_data[ChaptersTable.UNLOCKS.value],
			blocks=chapter_data[ChaptersTable.BLOCKS.value],
		)
