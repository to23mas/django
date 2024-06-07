from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from domain.data.projects_storage import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def overview(request: HttpRequest, course: str, sort_type: str) -> HttpResponse:
    """list all projects"""

    user_progress = get_progress_projects(request.user.username, course) #type: ignore

    if sort_type == 'all':
        projects_collection = list(find_projects_by_course(course))
    else:
        projects_collection = list(find_projects_by_course_and_ids(user_progress['projects'][sort_type], course)) #type: ignore

    # no projects in (lock, open, done, all)
    if not projects_collection:
        messages.warning(request, 'V této kategorii nebyli nalezeny žádné projekty.')

    return render(request, 'projects/overview.html', {
        'projects': projects_collection,
        'user_progress': user_progress,
        'course_name': course,
    })


@login_required
def detail(request: HttpRequest, course: str, project_no: int) -> HttpResponse:
    """detail view for projets"""

    project = get_project_detail(project_no, course)
    user_progress = get_progress_projects(request.user.username, course) #type: ignore

    # non exissting project
    if project == None:
        messages.error(request, 'Pokus o vstup do neexistujícího projektu!')
        return redirect('projects:overview', course=course, sort_type='all')

    # locked project
    if project_no in user_progress['projects']['lock']: #type: ignore
        messages.warning(request, 'Projekt ještě není odemčen!')
        return redirect('projects:overview', course=course, sort_type='all')

    lessons_progress = get_lesson_progress(request.user.username, project_no, course) #type: ignore
    return render(request, 'projects/detail.html', {
        'project': project,
        'lesson_progress': lessons_progress['lessons'][str(project_no)], #type: ignore
        'course_name': course,
    })
