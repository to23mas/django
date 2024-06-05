"""views.py"""
from domain.data.projects_storage import find_projects, get_progress_projects, find_projects_in
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


overview_html = 'overview/overview.html'
@login_required
def overview(request: HttpRequest) -> HttpResponse:
    """list all projects"""

    return render(request, overview_html, {
        'projects': find_projects(),
        'user_progress': get_progress_projects(request.user.username), #type: ignore
    })

def open(request: HttpRequest) -> HttpResponse:
    """list all projects"""

    progress = get_progress_projects(request.user.username),#type: ignore
    return render(request, overview_html, {
        'projects': find_projects_in(progress[0]['projects']['open']),#type: ignore
        'user_progress': progress[0],
    })

def done(request: HttpRequest) -> HttpResponse:
    """list all projects"""

    progress = get_progress_projects(request.user.username),#type: ignore
    return render(request, overview_html, {
        'projects': find_projects_in(progress[0]['projects']['done']),#type: ignore
        'user_progress': progress[0],
    })

def lock(request: HttpRequest) -> HttpResponse:
    """list all projects"""

    progress = get_progress_projects(request.user.username),#type: ignore
    return render(request, overview_html, {
        'projects': find_projects_in(progress[0]['projects']['lock']),#type: ignore
        'user_progress': progress[0],
    })
