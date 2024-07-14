from pymongo import MongoClient
from os import path, walk
import json


def clear_database(db):
    # db.lessons.delete_many({})
    # db.lessons.django.delete_many({})
    #
    # db.chapters.delete_many({})
    # db.chapters.django.delete_many({})
    #
    # db.progress.delete_many({})
    # db.progress.django.delete_many({})

    db.courses.delete_many({})
    #django
    db.projects.django.delete_many({})
    db.django.projects.delete_many({})
    db.django.lessons.delete_many({})
    db.django.chapters.delete_many({})
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
        db.django.lessons)
    ## chapters
    migrate(
        list_files('/usr/src/db/migrations/documents/courses/django/chapters/1/'),
        db.django.chapters)
    ## user progress
    migrate_one_file(
        '/usr/src/db/migrations/documents/user/admin-django-progress.json',
        db.django.progress)
    ## tests
    migrate(
        list_files('/usr/src/db/migrations/documents/courses/django/tests/'),
        db.django.tests)

    #inpv course
    migrate_one_file(
        '/usr/src/db/migrations/documents/courses/inpv/inpv.json',
        db.courses)

    #htmx course
    migrate_one_file(
        '/usr/src/db/migrations/documents/courses/htmx/htmx.json',
        db.courses)


    # project_files = list_files('/usr/src/db/migrations/documents/projects/')
    # lessons_files = list_files('/usr/src/db/migrations/documents/lessons/')
    # chapters_files = list_files('/usr/src/db/migrations/documents/chapters/')
    # progress_files = list_files('/usr/src/db/migrations/documents/user/')
    # courses_files = list_files('/usr/src/db/migrations/documents/courses/')
    #
    # migrate(project_files, db.projects.django)
    # migrate(lessons_files, db.lessons.django)
    # migrate(chapters_files, db.chapters.django)
    # migrate(progress_files, db.progress.django)
    # migrate(courses_files, db.courses)

    client.close()
