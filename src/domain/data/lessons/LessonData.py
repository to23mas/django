from dataclasses import dataclass
from typing import Dict, List
from bson.objectid import ObjectId


@dataclass
class LessonData():

	id: ObjectId
	no: int
	project: int
	title: str
	chapters: List[Dict[str, str|int]] | None
