"""views.py"""
from domain.data.projects_storage import find_projects, get_progress_projects, find_projects_in
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def overview(request: HttpRequest) -> HttpResponse:
    """list all projects"""

    return render(request, 'overview.html', {
        'projects': find_projects(),
        'user_progress': get_progress_projects(request.user.username),
    })

def open(request: HttpRequest) -> HttpResponse:
    """list all projects"""

    progress = get_progress_projects(request.user.username),
    return render(request, 'overview.html', {
        'projects': find_projects_in(progress[0]['projects']['open']),
        'user_progress': progress[0],
    })

def done(request: HttpRequest) -> HttpResponse:
    """list all projects"""

    progress = get_progress_projects(request.user.username),
    return render(request, 'overview.html', {
        'projects': find_projects_in(progress[0]['projects']['done']),
        'user_progress': progress[0],
    })

def lock(request: HttpRequest) -> HttpResponse:
    """list all projects"""

    progress = get_progress_projects(request.user.username),
    return render(request, 'overview.html', {
        'projects': find_projects_in(progress[0]['projects']['lock']),
        'user_progress': progress[0],
    })
