from pymongo import MongoClient
from os import listdir, path
import json
import psycopg2
from datetime import datetime

dir = '/usr/src/db/migrations/documents/projects/'
files = listdir(dir)

# psql
conn = psycopg2.connect(database="inpv", host="db", user="user", password="password", port="5432")
cursor = conn.cursor()

# mongo
client = MongoClient('mongodb', 27017)
db = client.inpv
projects = db.projects

for file in files:
    with open(dir + file) as f:
        file_data = json.load(f)
        filename = path.basename(f.name)
        cursor.execute(f"select * from django_migrations where name = '{filename}'")
        if cursor.fetchone() is None:
            projects.insert_one(file_data)
            cursor.execute(" INSERT INTO django_migrations values (99%s, %s, %s, %s)",
                           (int(path.basename(f.name).split('-')[0]), 'migrations', path.basename(f.name), datetime.now()))
            print(f'{filename} has been sucessfully migrated')
        else:
            print(f'{filename} already in DB')

conn.commit()
cursor.close()
conn.close()
client.close()
