from typing import Dict, List

from domain.data.projects.ProjectData import ProjectData
from domain.data.projects.tableDefinition.TableDefinitions import ProjectsTable


class ProjectDataSerializer:

	@staticmethod
	def to_dict(project_data: ProjectData) -> Dict[str, str | int | List[str]]:
		return {
			'_id': project_data.id,
			'database': project_data.database,
			'title': project_data.title,
			'description': project_data.description,
			'todo': project_data.todo,
		}


	@staticmethod
	def from_dict(project_data: dict) -> ProjectData:
		return ProjectData(
			id=project_data[ProjectsTable.ID.value],
			title=project_data[ProjectsTable.TITLE.value],
			description=project_data[ProjectsTable.DESCRIPTION.value],
			database=project_data[ProjectsTable.DATABASE.value],
			todo=project_data[ProjectsTable.TODO.value],
		)

