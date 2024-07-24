from dataclasses import dataclass
from typing import List


@dataclass
class ProjectData():

	id: int
	database: str
	title: str
	description: str
	todo: List[str]

