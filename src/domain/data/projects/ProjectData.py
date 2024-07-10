from dataclasses import dataclass
from typing import List


@dataclass
class ProjectData():

	no: int
	title: str
	description: str
	todo: List[str]

