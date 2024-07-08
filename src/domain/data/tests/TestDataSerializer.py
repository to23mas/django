from domain.data.tests.TestData import TestData
from domain.data.tests.tableDefinition.TableDefinitions import TestsTable


class TestDataSerializer:
    @staticmethod
    def from_array(testData: dict) -> TestData:
        return TestData(
            no=testData[TestsTable.NO.value],
            title=testData[TestsTable.TITLE.value],
            time=testData[TestsTable.TIME.value],
            description=testData[TestsTable.DESCRIPTION.value],
            target_type=testData[TestsTable.TARGET_TYPE.value],
            target_no=testData[TestsTable.TARGET_NO.value],
            attempts=testData[TestsTable.ATTEMPTS.value],
            success_score=testData[TestsTable.SUCCESS_SCORE.value],
        )

