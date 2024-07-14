from dataclasses import dataclass
from typing import Any, List
# from bson.objectid import ObjectId


@dataclass
class ProjectData():

	id: Any
	no: int
	title: str
	description: str
	todo: List[str]

