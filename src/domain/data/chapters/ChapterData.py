from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ChapterData():
	id: int
	lesson_id: int
	title: str
	unlock_type: str
	unlock_id: int
	unlocker_id: int
	is_last_in_lesson: bool
	blocks: List[Dict]
