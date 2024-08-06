from typing import Dict
from domain.Mongo import MongoStorage
from domain.data.exception.UnexpectedNoneResultException import UnexpectedNoneValueException


"""ALL"""
def get_content_progress(course: str, username: str, content: str) -> Dict :
	result = MongoStorage().database[course].progress.find(
		{ '_id': username },
		{ f'{content}': 1, '_id': 0 })

	return list(result)[0][content]


"""PROJECTS"""
def get_project_state(course: str, username: str, project_id: int) -> str :
	result = MongoStorage().database[course].progress.find_one(
		{"_id": username },{ f"projects.{str(project_id)}": 1, "_id": 0 }
	)
	if result == None: raise UnexpectedNoneValueException

	return result['projects'][str(project_id)]


def unlock_project(username: str, project_id: int) -> None:
	""" unlocks one project -> sets open"""

	MongoStorage().database.progress.update_one({
		'_id': username
	},{
		'$push': {f'projects.open': project_id},
		'$pull': {f'projects.lock': project_id}
	})


def finish_project(username: str, project_id: int) -> None:
	"""finish one project -> sets done"""

	MongoStorage().database.progress.update_one({
		'_id': username
	},{
		'$push': {f'projects.done': project_id},
		'$pull': {f'projects.open': project_id}
	})


"""LESSONS"""

def unlock_lesson(username: str, course: str, project_no: str, lesson_no: str) -> None:
	MongoStorage().database[course].progress.update_one({
		'_id': username
	}, {
		'$push': {f'lessons.{str(project_no)}.open': int(lesson_no)},
		 '$pull': {f'lessons.{str(project_no)}.lock': int(lesson_no)}
	})


def finish_lesson(username: str, course: str, project_no: str, lesson_no: str) -> None:
    ms = MongoStorage()

    ms.database[course].progress.update_one(
        {'_id': username},
        {'$push': {f'lessons.{str(project_no)}.open': int(lesson_no)},
         '$pull': {f'lessons.{str(project_no)}.lock': int(lesson_no)}})
