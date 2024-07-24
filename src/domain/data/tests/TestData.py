from dataclasses import dataclass

@dataclass
class TestData():

	id: int
	title: str
	time: int
	description: str
	target_type: str
	target_no: int
	source_no: int
	attempts: int
	success_score: float
	total_points: int
