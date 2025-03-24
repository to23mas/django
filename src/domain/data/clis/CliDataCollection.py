from typing import List

from pymongo.cursor import Cursor
from domain.data.clis.CliData import CliData
from domain.data.clis.CliDataSerializer import CliDataSerializer


class CliDataCollection:
	@staticmethod
	def from_dict(cli_data: dict|Cursor) -> List[CliData]:
		collection = []
		for c in cli_data:
			collection.append(CliDataSerializer.from_dict(c))
		return collection
