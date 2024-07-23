from dataclasses import dataclass
from typing import Dict

from bson.objectid import ObjectId


@dataclass
class ChapterData():
	id: ObjectId
	no: int
	project: int
	lesson: int
	title: str
	unlock_type: str
	unlock_no: str
	blocks: Dict
