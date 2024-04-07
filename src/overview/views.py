"""views.py"""
from domain.data.projects_storage import find_projects
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def overview(request: HttpRequest) -> HttpResponse:
    """list all projects"""

    return render(request, 'overview.html', {
        'projects': find_projects()
    })
