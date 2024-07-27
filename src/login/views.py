"""Wiews module"""
from django.views import generic
from pymongo import MongoClient


class IndexView(generic.TemplateView):
    """index view testing purposes"""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        client = MongoClient('localhost', 27017)
        db = client.inpv
        projects = db.projects.find({}, {"title": 1})
        return {"text": "ahoj"}
    # def get_queryset(self):
    #     return ['ahoj', 'nazdar']
