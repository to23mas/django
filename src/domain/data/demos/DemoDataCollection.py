from typing import List

from pymongo.cursor import Cursor
from domain.data.demos.DemoData import DemoData
from domain.data.demos.DemoDataSerializer import DemoDataSerializer


class DemoDataCollection:

	@staticmethod
	def from_dict(demo_data: dict|Cursor) -> List[DemoData]:
		collection = []
		for demo in demo_data:
			collection.append(DemoDataSerializer.from_dict(demo))
		return collection
