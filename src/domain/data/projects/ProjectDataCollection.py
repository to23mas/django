from typing import List

from pymongo.cursor import Cursor
from domain.data.projects.ProjectData import ProjectData
from domain.data.projects.ProjectDataSerializer import ProjectDataSerializer


class ProjectDataCollection:

	@staticmethod
	def from_array(testData: dict|Cursor) -> List[ProjectData]:
		collection = []
		for test in testData:
			collection.append(ProjectDataSerializer.from_dict(test))
		return collection

