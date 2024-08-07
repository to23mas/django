"""storage for projects"""
from typing import Dict, List

from bson.objectid import ObjectId
from domain.Mongo import MongoStorage
from domain.data.projects.ProjectData import ProjectData
from domain.data.projects.ProjectDataCollection import ProjectDataCollection
from domain.data.projects.ProjectDataSerializer import ProjectDataSerializer
from domain.data.projects.exception.UniqueDatabaseException import UniqueDatabaseException


def find_projects(db: str) -> List[ProjectData]:
	projects = MongoStorage().database[db].projects.find().sort('_id')
	return ProjectDataCollection.from_dict(projects)


def find_projects_by_course_and_ids(ids: list, db: str) -> List[ProjectData]:
	projects = MongoStorage().database[db].projects.find({"_id": {"$in": ids}}).sort('_id')
	return ProjectDataCollection.from_dict(projects)


def get_project_by_id(project_id: int, db: str) -> ProjectData | None:
	project = MongoStorage().database[db].projects.find_one({"_id": project_id})
	match project:
		case None: return None
		case _: return ProjectDataSerializer.from_dict(project)


def get_project(db: str, filter: Dict = {}) -> ProjectData | None:
	project = MongoStorage().database[db].projects.find_one(filter)
	match project:
		case None: return None
		case _: return ProjectDataSerializer.from_dict(project)


def create_project(project_data: ProjectData, db: str) -> None:
	project = get_project(db, {'database': project_data.database})
	match project:
		case None: MongoStorage().database[db].projects.insert_one(ProjectDataSerializer.to_dict(project_data))
		case _: raise UniqueDatabaseException


def delete_project(db: str, project_id: ObjectId) -> None:
	MongoStorage().database[db].projects.delete_one({'_id': project_id})


def exists_project(db: str, project_no: str) -> bool:
	res = MongoStorage().database[db].projects.find_one({'no': project_no})
	return True if res != None else False


def get_next_valid_id(db: str) -> int:
	document = MongoStorage().database[db].projects.find_one(sort=[('_id', -1)])
	match document:
		case None: return 1
		case _: return document['_id'] + 1


def update_project(project_data: ProjectData, db: str) -> None:
	MongoStorage().database[db].projects.update_one(
		{'_id': project_data.id},
		{'$set': ProjectDataSerializer.to_dict(project_data)}
	)
