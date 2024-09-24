from dataclasses import dataclass

@dataclass
class TestData():

	id: int
	title: str
	time: int
	description: str
	unlock_lesson: int
	unlock_chapter: int
	unlock_project: int
	finish_project: int
	finish_lesson: int
	finish_chapter: int
	attempts: int
	success_score: float
	total_points: int
