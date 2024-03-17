"""modgo database controller"""
from pymongo import MongoClient


class MongoStorage:

    def __init__(self):
        self.client = MongoClient('mongodb', 27017)
        self.database = self.client.inpv
