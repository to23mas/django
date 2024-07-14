from dataclasses import dataclass
from typing import Dict, List


@dataclass
class LessonData():

	no: int
	project: int
	title: str
	chapters: List[Dict[str, str|int]]

