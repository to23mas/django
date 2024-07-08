from typing import List

from pymongo.cursor import Cursor
from domain.data.tests.TestData import TestData
from domain.data.tests.TestDataSerializer import TestDataSerializer


class TestDataCollection:
    @staticmethod
    def from_array(testData: dict|Cursor) -> List[TestData]:
        collection = []
        for test in testData:
            collection.append(TestDataSerializer.from_array(test))
        return collection

