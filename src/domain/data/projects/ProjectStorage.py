"""storage for projects"""
from typing import Dict, List

from domain.Mongo import MongoStorage
from domain.data.projects.ProjectData import ProjectData
from domain.data.projects.ProjectDataCollection import ProjectDataCollection
from domain.data.projects.ProjectDataSerializer import ProjectDataSerializer
from domain.data.projects.exception.UniqueDatabaseException import UniqueDatabaseException

class ProjectStorage(MongoStorage):
	def __init__(self):
		super().__init__()


	def find_projects(self, db: str) -> List[ProjectData]:
		projects = self.database[db].projects.find().sort('_id')
		return ProjectDataCollection.from_dict(projects)


	def find_projects_by_course_and_ids(self, ids: list, db: str) -> List[ProjectData]:
		projects = self.database[db].projects.find({"_id": {"$in": ids}}).sort('_id')
		return ProjectDataCollection.from_dict(projects)


	def get_project_by_id(self, project_id: int, db: str) -> ProjectData | None:
		project = self.database[db].projects.find_one({"_id": project_id})
		match project:
			case None: return None
			case _: return ProjectDataSerializer.from_dict(project)


	def get_project(self, db: str, filter_: Dict = {}) -> ProjectData | None: #pylint: disable=W0102
		project = self.database[db].projects.find_one(filter_)
		match project:
			case None: return None
			case _: return ProjectDataSerializer.from_dict(project)


	def create_project(self, project_data: ProjectData, db: str) -> None:
		project = self.get_project(db, {'database': project_data.database})
		match project:
			case None: self.database[db].projects.insert_one(ProjectDataSerializer.to_dict(project_data))
			case _: raise UniqueDatabaseException


	def delete_project(self, db: str, project_id: int) -> None:
		self.database[db].projects.delete_one({'_id': project_id})


	def exists_project(self, db: str, project_no: str) -> bool:
		res = self.database[db].projects.find_one({'no': project_no})
		return res is not None


	def get_next_valid_id(self, db: str) -> int:
		document = self.database[db].projects.find_one(sort=[('_id', -1)])
		match document:
			case None: return 1
			case _: return document['_id'] + 1


	def update_project(self, project_data: ProjectData, db: str) -> None:
		self.database[db].projects.update_one(
			{'_id': project_data.id},
			{'$set': ProjectDataSerializer.to_dict(project_data)}
		)
