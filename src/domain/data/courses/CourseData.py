from dataclasses import dataclass
from typing import List

from bson.objectid import ObjectId


@dataclass
class CourseData():
	id: ObjectId
	order: int
	database: str
	title: str
	visible: bool
	open: bool
	description: str
	tags: List[str]
