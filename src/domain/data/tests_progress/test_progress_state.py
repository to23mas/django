from enum import Enum

class TestState(Enum):
    OPEN = 'open'
    CLOSE = 'close'
    FINISH = 'finish'
    DONE = 'done'
    FAIL = 'fail'
    SUCCESS = 'success'

    @staticmethod
    def from_string(value: str):
        if value == 'open':
            return TestState.OPEN
        if value == 'close':
            return TestState.CLOSE
        if value == 'finish':
            return TestState.FINISH
        if value == 'fail':
            return TestState.FAIL
        if value == 'success':
            return TestState.SUCCESS
        if value == 'done':
            return TestState.DONE
        return None

