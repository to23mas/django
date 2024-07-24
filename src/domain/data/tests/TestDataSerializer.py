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
			'target_no': test_data.target_no,
			'source_no': test_data.source_no,
			'attempts': test_data.attempts,
			'success_score': test_data.success_score,
			'total_points': test_data.total_points,
		}

	@staticmethod
	def from_array(testData: dict) -> TestData:
		return TestData(
			id=testData[TestsTable.ID.value],
			title=testData[TestsTable.TITLE.value],
			time=testData[TestsTable.TIME.value],
			description=testData[TestsTable.DESCRIPTION.value],
			target_type=testData[TestsTable.TARGET_TYPE.value],
			target_no=testData[TestsTable.TARGET_NO.value],
			source_no=testData[TestsTable.SOURCE_NO.value],
			attempts=testData[TestsTable.ATTEMPTS.value],
			success_score=testData[TestsTable.SUCCESS_SCORE.value],
			total_points=sum(
				question[TestQuestionTable.POINTS.value] for question in testData[TestsTable.QUESTIONS.value]
			)
		)
