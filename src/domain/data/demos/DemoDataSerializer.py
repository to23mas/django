from typing import Dict

from domain.data.demos.DemoData import DemoData
from domain.data.demos.tableDefinition.TableDefinitions import DemosTable


class DemoDataSerializer:

	@staticmethod
	def to_dict(demo_data: DemoData) -> Dict[str, str|int]:

		return {
			'_id': demo_data.id,
			'project_id': demo_data.project_id,
			'name': demo_data.name,
			'url': demo_data.url,
		}

	@staticmethod
	def from_dict(demo_data: dict) -> DemoData:

		return DemoData(
			id=demo_data[DemosTable.ID.value],
			project_id=demo_data[DemosTable.PROJECT_ID.value],
			name=demo_data[DemosTable.NAME.value],
			url=demo_data[DemosTable.URL.value],
		)
