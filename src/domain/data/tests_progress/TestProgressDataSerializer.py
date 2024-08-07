from domain.data.tests_progress.TestProgressData import TestProgressData
from domain.data.tests_progress.tableDefinition.TableDefinition import TestProgressTable


class TestProgressDataSerializer:
	@staticmethod
	def from_dict(progressData: dict) -> TestProgressData:
		return TestProgressData(
			test_no=progressData[TestProgressTable.TEST_ID.value],
			attempts=progressData[TestProgressTable.ATTEMPTS.value],
			state=progressData[TestProgressTable.STATE.value],
			score=progressData[TestProgressTable.SCORE.value],
		)

