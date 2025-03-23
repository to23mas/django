"""storage for CLI tasks"""
from typing import List

from domain.Mongo import MongoStorage
from domain.data.clis.CliData import CliData
from domain.data.clis.CliDataCollection import CliDataCollection
from domain.data.clis.CliDataSerializer import CliDataSerializer
from domain.data.clis.tableDefinition.TableDefinitions import CliTable


class CliStorage(MongoStorage):
    def get_cli(self, db: str, cli_id: int) -> CliData | None:
        cli = self.database[db].cli.find_one({
            CliTable.ID.value: cli_id,
        })
        match cli:
            case None: return None
            case _: return CliDataSerializer.from_dict(cli)

    def find_cli(self, db: str) -> List[CliData] | None:
        clis = self.database[db].cli.find().sort('_id')
        match clis:
            case None: return clis
            case _: return CliDataCollection.from_dict(clis)

    def create_cli(self, cli_data: CliData, db: str) -> None:
        self.database[db].cli.insert_one(CliDataSerializer.to_dict(cli_data))

    def delete_cli(self, db: str, cli_id: int) -> None:
        self.database[db].cli.delete_one({
            CliTable.ID.value: cli_id,
        })

    def update_cli(self, cli_data: CliData, db: str) -> None:
        self.database[db].cli.update_one(
            {
                CliTable.ID.value: cli_data.id,
            }, {'$set': CliDataSerializer.to_dict(cli_data)}
        )

    def get_next_valid_id(self, db: str) -> int:
        document = self.database[db].cli.find_one(
            sort=[(CliTable.ID.value, -1)]
        )

        match document:
            case None: return 1
            case _: return document[CliTable.ID.value] + 1
