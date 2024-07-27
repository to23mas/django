from typing import List
from domain.data.tests.QuestionDataSerializer import QuestionDataSerializer
from domain.data.tests.QuestionData import QuestionData


class QuestionDataCollection:
    @staticmethod
    def from_array(questionsData: dict) -> List[QuestionData]:
        collection = []
        for question in questionsData:
            collection.append(QuestionDataSerializer.from_dict(question))
        return collection
