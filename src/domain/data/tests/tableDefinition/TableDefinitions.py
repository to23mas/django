from enum import Enum

class TestsTable(Enum):

    ID = "_id"
    TITLE = "title"
    TIME = "time"
    DESCRIPTION = "description"
    TARGET_TYPE = "target_type"
    TARGET_ID = "target_id"
    SOURCE_ID = "source_id"
    ATTEMPTS = "attempts"
    SUCCESS_SCORE = "success_score"
    QUESTIONS = "questions"

class TestQuestionTable(Enum):

    QUESTION = "question"
    TYPE = "type"
    ANSWERS = "answers"
    CORRECT = "correct"
    POINTS = "points"
