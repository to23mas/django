from typing import List

from pymongo.cursor import Cursor
from domain.data.tests.TestData import TestData
from domain.data.tests.TestDataSerializer import TestDataSerializer


class TestDataCollection:

	@staticmethod
	def from_array(test_data: dict|Cursor) -> List[TestData]:
		collection = []
		for test in test_data:
			collection.append(TestDataSerializer.from_dict(test))
		return collection

