"""storage for lessons"""
from typing import List

import pymongo

from domain.Mongo import MongoStorage
from domain.data.demos.DemoData import DemoData
from domain.data.demos.DemoDataCollection import DemoDataCollection
from domain.data.demos.DemoDataSerializer import DemoDataSerializer
from domain.data.demos.tableDefinition.TableDefinitions import DemosTable
from domain.data.exception.DataNotFoundException import DataNotFoundException


def find_demos_for_overview(db: str, open_demos: list = []) -> List[DemoData]: #pylint: disable=W0102
	"""returns all test"""
	demos = MongoStorage().database[db].demos.find(
		{DemosTable.ID.value: {'$in': open_demos}}
	).sort(DemosTable.ID.value, pymongo.DESCENDING)

	if demos is None: raise DataNotFoundException

	return DemoDataCollection.from_dict(demos)


def get_demo(demo_id: int, db: str) -> DemoData | None:
	demo = MongoStorage().database[db].demos.find_one({
		"_id": demo_id,
	})

	match demo:
		case None: return None
		case _: return DemoDataSerializer.from_dict(demo)


def find_demos(db: str) -> List[DemoData] | None:
	demos = MongoStorage().database[db].demos.find().sort('_id')
	match demos:
		case None: return None
		case _: return DemoDataCollection.from_dict(demos)


def create_demo(demo_data: DemoData, db: str) -> None:
	MongoStorage().database[db].demos.insert_one(
		DemoDataSerializer.to_dict(demo_data)
	)


def delete_demo(db: str, demo_id: int) -> None:
	MongoStorage().database[db].demos.delete_one({'_id': demo_id})


def update_demo(demo_data: DemoData, db: str) -> None:
	MongoStorage().database[db].demos.update_one(
		{'_id': demo_data.id},
		{'$set': DemoDataSerializer.to_dict(demo_data)}
	)


def get_next_valid_id(db: str) -> int:
	document = MongoStorage().database[db].demos.find_one(
		sort=[(DemosTable.ID.value, -1)]
	)

	match document:
		case None: return 1
		case _: return document[DemosTable.ID.value] + 1
