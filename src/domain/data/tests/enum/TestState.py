from enum import Enum

class TestState(Enum):
	OPEN = 'open'
	CLOSE = 'close'
	FINISH = 'finish' # 100%
	FAIL = 'fail'
	SUCCESS = 'success'
