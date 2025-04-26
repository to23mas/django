from enum import Enum

class ExpectedTaskTypes(Enum):
	PRINT = 'print'
	CLASS = 'class'
	FUNCTION = 'function'
	VARIABLE = 'variable'
	VARIABLE_PATTERN = 'variable_pattern'
