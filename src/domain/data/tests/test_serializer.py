from domain.data.tests.test_data import QuestionData, TestData
from domain.data.tests.test_table_definition import TestQuestionTable, TestTable


class QuestionSerializer:
    @staticmethod
    def from_array(questionData: dict) -> QuestionData:
        return QuestionData(
            question=questionData[TestQuestionTable.QUESTION.value],
            type=questionData[TestQuestionTable.ATTEMPTS.value],
            answers=questionData[TestQuestionTable.ATTEMPTS.value],
            correct=questionData[TestQuestionTable.SCORE.value],
        )

class TestSerializer:
    @staticmethod
    def from_array(testData: dict) -> TestData:
        return TestData(
            no=testData[TestTable.NO.value],
            title=testData[TestTable.TITLE.value],
            time=testData[TestTable.TIME.value],
            description=testData[TestTable.DESCRIPTION.value],
            target_type=testData[TestTable.TARGET_TYPE.value],
            target_no=testData[TestTable.TARGET_NO.value],
            attempts=testData[TestTable.ATTEMPTS.value],
            success_score=testData[TestTable.SUCCESS_SCORE.value],
        )

