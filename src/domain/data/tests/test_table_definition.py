from enum import Enum

class TestTable(Enum):
    NO = "no"
    TITLE = "title"
    TIME = "time"
    DESCRIPTION = "description"
    TARGET_TYPE = "target_type"
    TARGET_NO = "target_no"
    ATTEMPTS = "attempts"
    SUCCESS_SCORE = "success_score"

    @staticmethod
    def from_string(value: str):
        if value == 'no':
            return TestProgressTable.NO
        if value == 'title':
            return TestProgressTable.TITLE
        if value == 'time':
            return TestProgressTable.TIME
        if value == 'description':
            return TestProgressTable.DESCRIPTION
        if value == 'target_type':
            return TestProgressTable.TARGET_TYPE
        if value == 'target_no':
            return TestProgressTable.TARGET_NO
        if value == 'attempts':
            return TestProgressTable.ATTEMPTS
        if value == 'success_score':
            return TestProgressTable.SUCCESS_SCORE

class TestQuestionTable(Enum):
    QUESTION = "question"
    TYPE = "type"
    ANSWERS = "answers"
    CORRECT = "correct"

    @staticmethod
    def from_string(value: str):
        if value == 'question':
            return TestQuestionTable.QUESTION
        if value == 'type':
            return TestQuestionTable.TYPE
        if value == 'answers':
            return TestQuestionTable.ANSWERS
        if value == 'correct':
            return TestQuestionTable.CORRECT
