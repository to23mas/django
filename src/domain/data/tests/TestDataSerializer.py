from typing import Dict
from domain.data.tests.TestData import TestData
from domain.data.tests.tableDefinition.TableDefinitions import TestQuestionTable, TestsTable


class TestDataSerializer:

	@staticmethod
	def to_dict(test_data: TestData) -> Dict[str, str | int | float]:
		return {
			'_id': test_data.id,
			'title': test_data.title,
			'time': test_data.time,
			'description': test_data.description,
			'finish_project': test_data.finish_project,
			'finish_lesson': test_data.finish_lesson,
			'finish_chapter': test_data.finish_chapter,
			'unlock_project': test_data.unlock_project,
			'unlock_lesson': test_data.unlock_lesson,
			'unlock_chapter': test_data.unlock_chapter,
			'current_project': test_data.current_project,
			'attempts': test_data.attempts,
			'success_score': test_data.success_score,
			'total_points': test_data.total_points,
		}

	@staticmethod
	def from_dict(testData: dict) -> TestData:
		try:
			total_points = sum(question[TestQuestionTable.POINTS.value] for question in testData[TestsTable.QUESTIONS.value])
		except: #pylint: disable=W0702
			total_points = 0

		return TestData(
			id=testData[TestsTable.ID.value],
			title=testData[TestsTable.TITLE.value],
			time=testData[TestsTable.TIME.value],
			description=testData[TestsTable.DESCRIPTION.value],
			unlock_chapter=testData[TestsTable.UNLOCK_CHAPTER.value],
			unlock_lesson=testData[TestsTable.UNLOCK_LESSON.value],
			unlock_project=testData[TestsTable.UNLOCK_PROJECT.value],
			finish_project=testData[TestsTable.FINISH_PROJECT.value],
			finish_lesson=testData[TestsTable.FINISH_LESSON.value],
			finish_chapter=testData[TestsTable.FINISH_CHAPTER.value],
			current_project=testData[TestsTable.CURRENT_PROJECT.value],
			attempts=testData[TestsTable.ATTEMPTS.value],
			success_score=testData[TestsTable.SUCCESS_SCORE.value],
			total_points=total_points,
		)
