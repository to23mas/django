"""migration script for mongo db to populate database with Django course data"""

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
	with open('/usr/src/db/Django a Client-Server aplikace.json') as f:
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

		for blockly in file_data['blockly']:
			database['django'].blockly.insert_one(blockly)

		for demo in file_data['demos']:
			database['django'].demos.insert_one(demo)

		for cli in file_data['clis']:
			database['django'].cli.insert_one(cli)

	print('[ ] - Migrating Users')
	with open('/usr/src/db/student.json') as f:
		file_data = json.load(f)
		database['django'].progress.insert_one(file_data)

	print('[x] - Migration DONE')
	client.close()
