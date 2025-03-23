from typing import Dict

from domain.data.clis.CliData import CliData
from domain.data.clis.tableDefinition.TableDefinitions import CliTable


class CliDataSerializer:
    @staticmethod
    def to_dict(cli_data: CliData) -> Dict[str, str | int]:
        return {
            '_id': cli_data.id,
            'title': cli_data.title,
            'task_description': cli_data.task_description,
            'expected_output': cli_data.expected_output,
        }

    @staticmethod
    def from_dict(cli_data: dict) -> CliData:
        return CliData(
            id=cli_data[CliTable.ID.value],
            title=cli_data[CliTable.TITLE.value],
            task_description=cli_data[CliTable.TASK_DESCRIPTION.value],
            expected_output=cli_data[CliTable.EXPECTED_OUTPUT.value],
        )
