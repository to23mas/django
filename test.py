## mongo test
# from pymongo import MongoClient
# client = MongoClient('localhost', 27017)
# db = client.inpv
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

