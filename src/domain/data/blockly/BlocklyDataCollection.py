from typing import List

from pymongo.cursor import Cursor
from domain.data.blockly.BlocklyData import BlocklyData
from domain.data.blockly.BlocklyDataSerializer import BlocklyDataSerializer


class BlocklyDataCollection:

	@staticmethod
	def from_dict(blockly_data: dict|Cursor) -> List[BlocklyData]:
		collection = []
		for b in blockly_data:
			collection.append(BlocklyDataSerializer.from_dict(b))
		return collection
