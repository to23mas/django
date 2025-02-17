"""storage for projects"""
from typing import List

from domain.Mongo import MongoStorage
from domain.data.blockly.BlocklyData import BlocklyData
from domain.data.blockly.BlocklyDataCollection import BlocklyDataCollection
from domain.data.blockly.BlocklyDataSerializer import BlocklyDataSerializer
from domain.data.blockly.tableDefinition.TableDefinitions import BlocklyTable


class BlocklyStorage(MongoStorage):
	def get_blockly(self, db: str, blockly_id: int) -> BlocklyData | None:
		blockly = self.database[db].blockly.find_one({
			BlocklyTable.ID.value: blockly_id,
		})
		match blockly:
			case None: return None
			case _: return BlocklyDataSerializer.from_dict(blockly)


	def find_blockly(self, db: str) -> List[BlocklyData] | None:
		blocklys = self.database[db].blockly.find().sort('_id')
		match blocklys:
			case None: return blocklys
			case _: return BlocklyDataCollection.from_dict(blocklys)


	def create_blockly(self, blockly_data: BlocklyData, db: str) -> None:
		self.database[db].blockly.insert_one(BlocklyDataSerializer.to_dict(blockly_data))


	def delete_blockly(self, db: str, blockly_id: int) -> None:
		self.database[db].blockly.delete_one({
			BlocklyTable.ID.value: blockly_id,
		})


	def update_blockly(self, blockly_data: BlocklyData, db: str) -> None:
		self.database[db].blockly.update_one(
			{
				BlocklyTable.ID.value: blockly_data.id,
			}, {'$set': BlocklyDataSerializer.to_dict(blockly_data)}
		)


	def get_next_valid_id(self, db: str) -> int:
		document = self.database[db].blockly.find_one(
			sort=[(BlocklyTable.ID.value, -1)]
		)

		match document:
			case None: return 1
			case _: return document[BlocklyTable.ID.value] + 1
