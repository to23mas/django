from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from domain.data.projects_storage import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

overview_html = 'overview/overview.html'
@login_required
def overview(request: HttpRequest, course: str, sort_type: str) -> HttpResponse:
    """list all projects"""

    return render(request, overview_html, {
        'projects': find_projects(course),
        'user_progress': get_progress_projects(request.user.username), #type: ignore
    })

# @login_required
# def project_detail(request: HttpRequest, project_id: int) -> HttpResponse:
#     """detail view for projets"""
#
#     project = get_project_detail(project_id)
#
#     # non exissting project
#     if project == None:
#         messages.error(request, 'Pokus o vstup do neexistujícího projektu!')
#         return redirect('overview:overview')
#
#     # locked project
#     if project_id in get_progress_projects(request.user.username)['projects']['lock']: #type: ignore
#         messages.warning(request, 'Projekt ještě není odemčen!')
#         return redirect('overview:overview')
#
#     lessons_progress = get_lesson_progress(request.user.username, project_id) #type: ignore
#     return render(request, 'project_detail.html', {
#         'project': project,
#         'lesson_progress': lessons_progress['lessons'][str(project_id)], #type: ignore
#     })
#
