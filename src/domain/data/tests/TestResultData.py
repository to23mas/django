from dataclasses import dataclass


@dataclass
class TestResultData():
	success: bool
	score_percentage: float
	score_total: int
	target_unlock_type: str
	target_id: int
	source_id: int
