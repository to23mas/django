from typing import List

from pymongo.cursor import Cursor
from domain.data.chapters.ChapterData import ChapterData
from domain.data.chapters.ChapterDataSerializer import ChapterDataSerializer


class ChapterDataCollection:

	@staticmethod
	def from_dict(chapter_data: dict|Cursor) -> List[ChapterData]:
		collection = []
		for chapter in chapter_data:
			collection.append(ChapterDataSerializer.from_dict(chapter))
		return collection
