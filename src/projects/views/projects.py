from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.progress_storage import get_lesson_progress, get_user_progress_by_course
from domain.data.projects_storage import find_projects_by_course, find_projects_by_course_and_ids, get_project_detail


@login_required
def overview(request: HttpRequest, course: str, sort_type: str) -> HttpResponse:
    """list all projects"""

    username = request.user.username #type: ignore
    user_progress = get_user_progress_by_course(username, course)

    if sort_type == 'all':
        projects_collection = list(find_projects_by_course(course))
    else:
        projects_collection = list(find_projects_by_course_and_ids(user_progress['projects'][sort_type], course))

    # no projects in (lock, open, done, all)
    if not projects_collection:
        messages.warning(request, 'V tomto kurzu nebyly nalezeny žádné projekty.')

    return render(request, 'projects/overview.html', {
        'projects': projects_collection,
        'user_progress': user_progress,
        'course_name': course,
    })


@login_required
def detail(request: HttpRequest, course: str, project_no: int) -> HttpResponse:
    """detail view for projets"""

    username = request.user.username #type: ignore
    user_progress = get_user_progress_by_course(username, course)

    project = get_project_detail(project_no, course)

    # non exissting project
    if project == None:
        messages.error(request, 'Pokus o vstup do neexistujícího projektu!')
        return redirect('projects:overview', course=course, sort_type='all')

    # locked project
    if project_no in user_progress['projects']['lock']:
        messages.warning(request, 'Projekt ještě není odemčen!')
        return redirect('projects:overview', course=course, sort_type='all')

    # need this to build the lesson graph
    lessons_progress = get_lesson_progress(username, project_no, course)
    return render(request, 'projects/detail.html', {
        'project': project,
        'lesson_progress': lessons_progress['lessons'][str(project_no)],
        'course_name': course,
    })
