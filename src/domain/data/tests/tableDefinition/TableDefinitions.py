from enum import Enum

class TestsTable(Enum):

    NO = "no"
    TITLE = "title"
    TIME = "time"
    DESCRIPTION = "description"
    TARGET_TYPE = "target_type"
    TARGET_NO = "target_no"
    ATTEMPTS = "attempts"
    SUCCESS_SCORE = "success_score"
    QUESTIONS = "questions"

class TestQuestionTable(Enum):

    QUESTION = "question"
    TYPE = "type"
    ANSWERS = "answers"
    CORRECT = "correct"
    POINTS = "points"
