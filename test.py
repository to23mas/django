## mongo test
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.inpv
# for project in db.projects.find():
#     print(project)


## postgresql
# import psycopg2
# import pprint
# from datetime import datetime
#
# conn = psycopg2.connect(database="inpv",
#                         host="localhost",
#                         user="user",
#                         password="password",
#                         port="5432")
#
# cursor = conn.cursor()
# cursor.execute("INSERT INTO django_migrations values (88, %s, %s, %s);",
#                ('ahoj', 'ahoj', datetime.now()))
# cursor.execute('select * from django_migrations')
# pprint.pp(cursor.fetchall())


# unlock_project('admin', 2000, True)
username = 'admin'
unlock = True
project_id = 2000
repository = 'lessons'
parent_id = 1000
updated_item_id = 1300

to_add = 'open' if unlock else 'done'
to_rem = 'lock' if unlock else 'open'

print(db.progress.find_one({'_id': 'admin'}))
print(db.progress.update_one(
    {
        '_id': username
    },{
        '$push': {f'{repository}.{parent_id}.{to_add}': updated_item_id},
        '$pull': {f'{repository}.{parent_id}.{to_rem}': updated_item_id},
    }))
