from dataclasses import dataclass
from typing import Dict, List


@dataclass
class LessonData():

	id:int
	title: str
	chapters: List[Dict[str, str|int]] | None
