"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from domain.data.projects_storage import ProjectsStorage
from django.contrib.auth.decorators import login_required


@login_required
def project_detail(request: HttpRequest, project_no: int) -> HttpResponse:
    """detail view for projets"""

    return render(request, 'project_detail.html', {
        'project': ProjectsStorage.getDetail(project_no)
    })
