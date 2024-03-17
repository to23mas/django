"""views.py"""
from django.views.generic import TemplateView
from domain.data.projects_storage import ProjectsStorage
from django.contrib.auth.mixins import LoginRequiredMixin


class Overview(LoginRequiredMixin, TemplateView):
    """index view testing purposes"""
    login_url = "/login"
    template_name = 'overview.html'

    def get_context_data(self, **kwargs):
        return {'projects': ProjectsStorage.findTitles()}
