from typing import List
from domain.data.tests.test_data import QuestionData, TestData
from domain.data.tests.test_serializer import QuestionSerializer, TestSerializer


class TestCollection:
    @staticmethod
    def from_array(testData: dict) -> List[TestData]:
        collection = []
        for test in testData:
            collection.append(TestSerializer.from_array(test))
        return collection

class QuestionsCollection:
    @staticmethod
    def from_array(questionsData: dict) -> List[QuestionData]:
        collection = []
        for question in questionsData:
            collection.append(QuestionSerializer.from_array(question))
        return collection


