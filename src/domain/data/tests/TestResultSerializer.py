from typing import Dict

from domain.data.tests.TestResultData import TestResultData


class TestResultSerializer:

	@staticmethod
	def to_array(test_result_data: TestResultData) -> Dict[str, str|bool|float|int]:
		return {
			"success": test_result_data.success,
			"score_percentage": test_result_data.score_percentage,
			"score_total": test_result_data.score_total,
		}
