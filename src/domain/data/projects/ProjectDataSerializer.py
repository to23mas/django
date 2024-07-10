from domain.data.projects.ProjectData import ProjectData
from domain.data.projects.tableDefinition.TableDefinitions import ProjectsTable


class ProjectDataSerializer:

	@staticmethod
	def from_array(project_data: dict) -> ProjectData:

		return ProjectData(
			no=project_data[ProjectsTable.NO.value],
			title=project_data[ProjectsTable.TITLE.value],
			description=project_data[ProjectsTable.DESCRIPTION.value],
			todo=project_data[ProjectsTable.TODO.value],
		)

