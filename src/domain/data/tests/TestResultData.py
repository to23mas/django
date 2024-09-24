from dataclasses import dataclass


@dataclass
class TestResultData():
	success: bool
	score_percentage: float
	score_total: int
