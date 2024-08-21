from typing import Dict

from domain.data.blockly.BlocklyData import BlocklyData
from domain.data.blockly.tableDefinition.TableDefinitions import BlocklyTable


class BlocklyDataSerializer:

	@staticmethod
	def to_dict(blockly_data: BlocklyData) -> Dict[str, str | int | Dict]:
		return {
			'_id': blockly_data.id,
			'title': blockly_data.title,
			'toolbox': blockly_data.toolbox,
			'expected_task': blockly_data.expected_task,
			'expected_result': blockly_data.expected_result,
		}


	@staticmethod
	def from_dict(blockly_data: dict) -> BlocklyData:
		return BlocklyData(
			id=blockly_data[BlocklyTable.ID.value],
			title=blockly_data[BlocklyTable.TITLE.value],
			expected_task=blockly_data[BlocklyTable.EXPECTED_TASK.value],
			expected_result=blockly_data[BlocklyTable.EXPECTED_RESULT.value],
			toolbox=blockly_data[BlocklyTable.TOOLBOX.value],
		)
