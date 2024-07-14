from dataclasses import dataclass
from typing import List


@dataclass
class CourseData():

	order: int
	no: int
	title: str
	projects: str
	visible: bool
	open: bool
	description: str
	tags: List[str]
