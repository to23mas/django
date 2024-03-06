"""Wiews module"""
from django.views import generic


class IndexView(generic.TemplateView):
    """index view testing purposes"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return {'text': ['ahoj', 'nazdar', 'bazar']}
    # def get_queryset(self):
    #     return ['ahoj', 'nazdar']
