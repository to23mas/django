from dataclasses import dataclass
from typing import Dict


@dataclass
class ChapterData():
	id: int
	lesson_id: int
	title: str
	unlock_type: str
	unlock_id: str
	blocks: Dict
