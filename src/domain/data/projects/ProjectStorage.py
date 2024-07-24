"""storage for projects"""
from typing import List, Tuple

from bson.objectid import ObjectId
from domain.Mongo import MongoStorage
from domain.data.projects.ProjectData import ProjectData
from domain.data.projects.ProjectDataCollection import ProjectDataCollection
from domain.data.projects.ProjectDataSerializer import ProjectDataSerializer


def find_projects(db: str) -> List[ProjectData]:
	projects = MongoStorage().database[db].projects.find().sort('_id')
	return ProjectDataCollection.from_array(projects)


def find_projects_by_course_and_ids(ids: list, db: str) -> List[ProjectData]:
	projects = MongoStorage().database[db].projects.find({"no": {"$in": ids}}).sort('_id')

	return ProjectDataCollection.from_array(projects)


def get_project(project_id: int, db: str) -> Tuple[ProjectData | None, List | None]:
	project = MongoStorage().database[db].projects.find_one({"_id": project_id})
	if project == None: return (None, None)

	return (ProjectDataSerializer.from_dict(project), project.get('lessons'))


def create_project(project_data: ProjectData, db: str) -> None:
	MongoStorage().database[db].projects.insert_one(ProjectDataSerializer.to_dict(project_data))


def delete_project(db: str, project_id: ObjectId) -> None:
	MongoStorage().database[db].projects.delete_one({'_id': project_id})


def exists_project(db: str, project_no: str) -> bool:
	res = MongoStorage().database[db].projects.find_one({'no': project_no})
	return True if res != None else False

