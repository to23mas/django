from domain.data.tests_progress.test_progress_data import TestProgress
from domain.data.tests_progress.test_progress_table_definition import TestProgressTable


class TestProgressSerializer:
    @staticmethod
    def from_array(progressData: dict) -> TestProgress:
        return TestProgress(
            test_no=progressData[TestProgressTable.TEST_NO.value],
            attempts=progressData[TestProgressTable.ATTEMPTS.value],
            state=progressData[TestProgressTable.STATE.value],
            score=progressData[TestProgressTable.SCORE.value],
        )

