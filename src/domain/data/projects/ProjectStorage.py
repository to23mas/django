"""storage for projects"""
from typing import List, Tuple
from domain.Mongo import MongoStorage
from domain.data.projects.ProjectData import ProjectData
from domain.data.projects.ProjectDataCollection import ProjectDataCollection
from domain.data.projects.ProjectDataSerializer import ProjectDataSerializer


def find_projects_by_course(course: str) -> List[ProjectData]:
	projects = MongoStorage().database[course].projects.find().sort('no')
	return ProjectDataCollection.from_array(projects)


def find_projects_by_course_and_ids(ids: list, course: str) -> List[ProjectData]:
	projects = MongoStorage().database[course].projects.find({"no": {"$in": ids}}).sort('no')

	return ProjectDataCollection.from_array(projects)


def get_project(project_no: int, course: str) -> Tuple[ProjectData | None, List | None]:
	project = MongoStorage().database[course].projects.find_one({"no": project_no})
	if project == None: return (None, None)

	return (ProjectDataSerializer.from_array(project), project['lessons'])


def get_locked_projects(username: str):
	ms = MongoStorage()
	return ms.database.progress.find_one({"_id": username}, {"projects": 1})

