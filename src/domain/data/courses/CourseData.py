from dataclasses import dataclass
from typing import List


@dataclass
class CourseData():

	id: int
	order: int
	database: str
	title: str
	visible: bool
	open: bool
	description: str
	tags: List[str]
