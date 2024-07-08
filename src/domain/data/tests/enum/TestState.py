from enum import Enum

class TestState(Enum):
    OPEN = 'open'
    CLOSE = 'close'
    FINISH = 'finish'
    FAIL = 'fail'
    SUCCESS = 'success'
