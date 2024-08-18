from pymongo import MongoClient
from os import path, walk
import json


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
	database = client.inpv
	client.drop_database("inpv")

	print('[ ] - Migrating Django Course')
	with open('/usr/src/db/migrations/documents/courses/django/Django.json') as f:
		file_data = json.load(f)
		course_data = file_data['course']
		database.courses.insert_one(course_data)

		for project in file_data['projects']:
			database['django'].projects.insert_one(project)
			for lesson in project['lessons']:
				database['django'].project[project['database']].lessons.insert_one(lesson)
			for chapter in project['chapters']:
				database['django'].project[project['database']].chapters.insert_one(chapter)

		for test in file_data['tests']:
			database['django'].tests.insert_one(test)
			for question in test['questions']:
				database['django'].tests.update_one(
					{'_id': test['_id']},
					{'$push': {'questions': question}})

		for blockly in file_data['blockly']:
			database['django'].blockly.insert_one(blockly)

	client.close()
	print('[x] - Migration DONE')

	# #django course
	# django_course = migrate_one_file(
	# 	'/usr/src/db/migrations/documents/courses/django/django.json',
	# 	db.courses)
	# ## projects
	# migrate(
	# 	list_files('/usr/src/db/migrations/documents/courses/django/projects/'),
	# 	db.django.projects)
	# ## lessons
	# migrate(
	# 	list_files('/usr/src/db/migrations/documents/courses/django/lessons/1/'),
	# 	db.django.project.project_1.lessons)
	# ## chapters
	# migrate(
	# 	list_files('/usr/src/db/migrations/documents/courses/django/chapters/1/'),
	# 	db.django.project.project_1.chapters)
	# migrate(
	# 	list_files('/usr/src/db/migrations/documents/courses/django/chapters/2/'),
	# 	db.django.project.project_1.chapters)
	# ## user progress
	# # migrate_one_file(
	# # 	'/usr/src/db/migrations/documents/user/admin-django-progress.json',
	# # 	db.django_testing.progress)
	# ## tests
	# migrate(
	# 	list_files('/usr/src/db/migrations/documents/courses/django/tests/1/'),
	# 	db.django.tests)
	# ## user progress
