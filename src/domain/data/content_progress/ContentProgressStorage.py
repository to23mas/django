from typing import Dict
from domain.Mongo import MongoStorage
from domain.data.exception.UnexpectedNoneResultException import UnexpectedNoneValueException


"""ALL"""
def get_content_progress(db: str, username: str, content: str) -> Dict :
	result = MongoStorage().database[db].progress.find(
		{ '_id': username },
		{ f'{content}': 1, '_id': 0 })

	ret_res = list(result)
	if ret_res == []:
		return {}
	return ret_res[0][content]


"""PROJECTS"""
def get_project_state(course: str, username: str, project_id: int) -> str :
	result = MongoStorage().database[course].progress.find_one(
		{"_id": username },{ f"projects.{str(project_id)}": 1, "_id": 0 }
	)
	if result == None: raise UnexpectedNoneValueException

	return result['projects'][str(project_id)]


def unlock_project(course: str, username: str, project_id: int) -> None:
	""" unlocks one project -> sets open"""

	MongoStorage().database[course].progress.update_one({
		'_id': username
	},{
		'$push': {f'projects.open': project_id},
		'$pull': {f'projects.lock': project_id}
	})


def finish_project(course: str, username: str, project_id: int) -> None:
	"""finish one project -> sets done"""

	MongoStorage().database[course].progress.update_one({
		'_id': username
	},{
		'$push': {f'projects.done': project_id},
		'$pull': {f'projects.open': project_id}
	})


"""LESSONS"""
def get_lesson_state(db: str, username: str, lesson_id: int) -> str :
	result = MongoStorage().database[db].progress.find_one(
		{"_id": username },{ f"lessons.{str(lesson_id)}": 1, "_id": 0 }
	)
	if result == None: raise UnexpectedNoneValueException

	return result['lessons'][str(lesson_id)]






"""Chapters"""
def get_chapter_state(db: str, username: str, chapter_id: int) -> str :
	result = MongoStorage().database[db].progress.find_one(
		{"_id": username },{ f"chapters.{str(chapter_id)}": 1, "_id": 0 }
	)
	if result == None: raise UnexpectedNoneValueException

	return result['chapters'][str(chapter_id)]
