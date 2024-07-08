from enum import Enum

class TestProgressTable(Enum):
    TEST_NO = 'test_no'
    ATTEMPTS = 'attempts'
    STATE = 'state'
    SCORE = 'score'

    @staticmethod
    def from_string(value: str):
        if value == 'test_no':
            return TestProgressTable.TEST_NO
        if value == 'attempts':
            return TestProgressTable.ATTEMPTS
        if value == 'state':
            return TestProgressTable.STATE
        if value == 'score':
            return TestProgressTable.SCORE
        return None
