from typing import List

from pymongo.cursor import Cursor
from domain.data.chapters.ChapterData import ChapterData
from domain.data.chapters.ChapterDataSerializer import ChapterDataSerializer


class ChapterDataCollection:

	@staticmethod
	def from_array(chapter_data: dict|Cursor) -> List[ChapterData]:
		collection = []
		for chapter in chapter_data:
			__import__('pprint').pprint(chapter)
			collection.append(ChapterDataSerializer.from_array(chapter))
		return collection
