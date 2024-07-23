from typing import Dict, List

from bson.objectid import ObjectId
from domain.data.projects.ProjectData import ProjectData
from domain.data.projects.tableDefinition.TableDefinitions import ProjectsTable


class ProjectDataSerializer:

	@staticmethod
	def to_dict(project_data: ProjectData) -> Dict[str, ObjectId | str | int | List[str]]:
		return {
			'_id': ObjectId(project_data.id),
			'no': project_data.no,
			'title': project_data.title,
			'description': project_data.description,
			'todo': project_data.todo,
		}


	@staticmethod
	def from_dict(project_data: dict) -> ProjectData:
		return ProjectData(
			id=project_data[ProjectsTable.ID.value],
			no=project_data[ProjectsTable.NO.value],
			title=project_data[ProjectsTable.TITLE.value],
			description=project_data[ProjectsTable.DESCRIPTION.value],
			todo=project_data[ProjectsTable.TODO.value],
		)

