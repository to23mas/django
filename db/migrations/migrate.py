from pymongo import MongoClient
from os import path, walk
import json


def clear_database(db):
    db.projects.delete_many({})
    db.lessons.delete_many({})
    db.chapters.delete_many({})
    

def list_files(directory):
    file_list = []
    for root, _, files in walk(directory):
        for filename in files:
            file_list.append(path.join(root, filename))
    return file_list


def migrate(files, collection):
    for file in files:
        with open(file) as f:
            file_data = json.load(f)
            filename = path.basename(f.name)
            collection.insert_one(file_data)
            print(f'{filename} -> migrated')


if __name__ == "__main__":
    client = MongoClient('mongodb', 27017)
    db = client.inpv

    clear_database(db)

    project_files = list_files('/usr/src/db/migrations/documents/projects/')
    lessons_files = list_files('/usr/src/db/migrations/documents/lessons/')
    chapters_files = list_files('/usr/src/db/migrations/documents/chapters/')

    migrate(project_files, db.projects)
    migrate(lessons_files, db.lessons)
    migrate(chapters_files, db.chapters)

    client.close()
