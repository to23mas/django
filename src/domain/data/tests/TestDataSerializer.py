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
			'target_type': test_data.target_type,
			'target_id': test_data.target_id,
			'source_id': test_data.source_id,
			'attempts': test_data.attempts,
			'success_score': test_data.success_score,
			'total_points': test_data.total_points,
		}

	@staticmethod
	def from_dict(testData: dict) -> TestData:
		try:
			total_points = sum(question[TestQuestionTable.POINTS.value] for question in testData[TestsTable.QUESTIONS.value])
		except:
			total_points = 0

		return TestData(
			id=testData[TestsTable.ID.value],
			title=testData[TestsTable.TITLE.value],
			time=testData[TestsTable.TIME.value],
			description=testData[TestsTable.DESCRIPTION.value],
			target_type=testData[TestsTable.TARGET_TYPE.value],
			target_id=testData[TestsTable.TARGET_ID.value],
			source_id=testData[TestsTable.SOURCE_ID.value],
			attempts=testData[TestsTable.ATTEMPTS.value],
			success_score=testData[TestsTable.SUCCESS_SCORE.value],
			total_points=total_points,
		)
