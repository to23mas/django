from pymongo import MongoClient
from os import path, walk
import json


def clear_database(db):
	db.courses.delete_one({'_id': 1})
	db.courses.delete_one({'_id': 2})

	db.django.projects.delete_many({})
	db.django.project.project_1.chapters.delete_many({})
	db.django.project.project_1.lessons.delete_many({})
	db.django.progress.delete_many({})
	db.django.tests.delete_many({})


def list_files(directory):
	file_list = []
	for root, _, files in walk(directory):
		for filename in files:
			file_list.append(path.join(root, filename))
	return file_list


def migrate(files, collection):
	for file in files:
		print('migrating -> ', file)
		with open(file) as f:
			file_data = json.load(f)
			filename = path.basename(f.name)
			collection.insert_one(file_data)
			print(f'{filename} -> migrated')

def migrate_one_file(file, collection):
	print('migrating -> ', file)
	with open(file) as f:
		file_data = json.load(f)
		filename = path.basename(f.name)
		collection.insert_one(file_data)
		print(f'{filename} -> migrated')

if __name__ == "__main__":
	client = MongoClient('mongodb', 27017)
	db = client.inpv

	clear_database(db)
	#django course
	django_course = migrate_one_file(
		'/usr/src/db/migrations/documents/courses/django/django.json',
		db.courses)
	## projects
	migrate(
		list_files('/usr/src/db/migrations/documents/courses/django/projects/'),
		db.django.projects)
	## lessons
	migrate(
		list_files('/usr/src/db/migrations/documents/courses/django/lessons/1/'),
		db.django.project.project_1.lessons)
	## chapters
	migrate(
		list_files('/usr/src/db/migrations/documents/courses/django/chapters/1/'),
		db.django.project.project_1.chapters)
	## user progress
	# migrate_one_file(
	# 	'/usr/src/db/migrations/documents/user/admin-django-progress.json',
	# 	db.django_testing.progress)
	## tests
	migrate(
		list_files('/usr/src/db/migrations/documents/courses/django/tests/1/'),
		db.django.tests)
	## user progress
	client.close()
