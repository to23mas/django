"""storage for projects"""
from pymongo.cursor import Cursor
from domain.Mongo import MongoStorage


def find_courses() -> Cursor:
    ms = MongoStorage()
    return ms.database.courses.find().sort('order')
