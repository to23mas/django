from domain.data.chapters.ChapterData import ChapterData
from domain.data.chapters.tableDefinition.TableDefinitions import ChaptersTable


class ChapterDataSerializer:

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
