from dataclasses import dataclass
from typing import List
from bson.objectid import ObjectId


@dataclass
class ProjectData():

	id: ObjectId
	no: int
	title: str
	description: str
	todo: List[str]

