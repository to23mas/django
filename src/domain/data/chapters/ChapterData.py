from dataclasses import dataclass
from typing import Dict


@dataclass
class ChapterData():

	no: int
	project: int
	lesson: int
	title: str
	unlocks: Dict[str, str]
	blocks: Dict

