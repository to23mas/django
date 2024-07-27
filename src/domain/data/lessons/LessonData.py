from dataclasses import dataclass
from typing import List


@dataclass
class LessonData():

	id: int
	title: str
	to: List[int]
