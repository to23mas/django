from enum import Enum

class TestsTable(Enum):

    ID = "_id"
    TITLE = "title"
    TIME = "time"
    DESCRIPTION = "description"
    UNLOCK_CHAPTER = "unlock_chapter"
    UNLOCK_LESSON = "unlock_lesson"
    UNLOCK_PROJECT = "unlock_project"
    FINISH_CHAPTER = "finish_chapter"
    FINISH_LESSON = "finish_lesson"
    FINISH_PROJECT = "finish_project"
    ATTEMPTS = "attempts"
    SUCCESS_SCORE = "success_score"
    QUESTIONS = "questions"

class TestQuestionTable(Enum):

    ID = "_id"
    QUESTION = "question"
    TYPE = "type"
    ANSWERS = "answers"
    CORRECT = "correct"
    POINTS = "points"
