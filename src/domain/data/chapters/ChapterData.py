from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ChapterData():
	id: int
	lesson_id: int
	title: str
	unlock_type: str
	unlock_id: int
	blocks: List[Dict]
