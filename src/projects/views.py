"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from domain.data.projects_storage import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# overview_html = 'overview/overview.html'
# @login_required
# def overview(request: HttpRequest, course: str, sort_type: str) -> HttpResponse:
#     """list all projects"""
#
#     return render(request, overview_html, {
#         'projects': find_projects(course),
#         'user_progress': get_progress_projects(request.user.username), #type: ignore
#     })

@login_required
def project_detail(request: HttpRequest, project_id: int) -> HttpResponse:
    """detail view for projets"""

    project = get_project_detail(project_id)

    # non exissting project
    if project == None:
        messages.error(request, 'Pokus o vstup do neexistujícího projektu!')
        return redirect('overview:overview')

    # locked project
    if project_id in get_progress_projects(request.user.username)['projects']['lock']: #type: ignore
        messages.warning(request, 'Projekt ještě není odemčen!')
        return redirect('overview:overview')

    lessons_progress = get_lesson_progress(request.user.username, project_id) #type: ignore
    return render(request, 'project_detail.html', {
        'project': project,
        'lesson_progress': lessons_progress['lessons'][str(project_id)], #type: ignore
    })


@login_required
def lesson(request: HttpRequest, project_id: int, lesson_id: int, chapter_id: int) -> HttpResponse:
    """display lesson"""

    lesson = get_lesson(lesson_id)
    chapter = get_chapter(chapter_id)

    # non exissting lesson or chapter
    if lesson == None or chapter == None:
        messages.error(request, 'Pokus o vstup k neexistujícím zdrojům!')
        return redirect('overview:overview')

    # locked lesson or chapter
    progress = get_progress_projects(request.user.username) #type: ignore
    if lesson_id in progress['lessons'][str(project_id)]['lock'] or chapter_id in progress['chapters'][str(lesson_id)]['lock']: #type: ignore
        messages.warning(request, 'Lekce/kapitola ještě není odemčena!')
        return redirect('overview:overview')

    return render(request, 'lesson.html', {
        'project_id': project_id,
        'lesson': lesson,
        'chapter': chapter,
        'chapter_finished': chapter_id in progress['chapters'][str(lesson_id)]['done'], #type: ignore
        'sidebar_progress': progress['chapters'][str(lesson_id)], #type: ignore
        'chapter_id': chapter_id,
    })


@login_required
def next_chapter(request: HttpRequest) -> HttpResponse:
    """display lesson"""

    next_chapter_id = int(request.POST.get('chapter_id')) + 1 #type: ignore
    lesson_id = next_chapter_id - (next_chapter_id % 100)
    project_id = next_chapter_id - (next_chapter_id % 1000)

    if (get_chapter(next_chapter_id) == None):
        return redirect('projects:lesson', lesson_id=(lesson_id + 100), chapter_id=(lesson_id+1))

    return redirect('projects:lesson', project_id=project_id, lesson_id=lesson_id, chapter_id=next_chapter_id)


@login_required
def unlock_chapter(request: HttpRequest) -> HttpResponse:
    """display lesson"""

    next_chapter_id = int(request.POST.get('chapter_id')) + 1 #type: ignore
    lesson_id = next_chapter_id - (next_chapter_id % 100)
    project_id = next_chapter_id - (next_chapter_id % 1000)

    progress_lesson_or_chapter(request.user.username, next_chapter_id, lesson_id, unlock=True, lesson=False) #type: ignore
    progress_lesson_or_chapter(request.user.username, (next_chapter_id-1), lesson_id, unlock=False, lesson=False) #type: ignore

    if (get_chapter(next_chapter_id) == None):
        # TODO may -> redirect to the next lesson/project instead of overview
        return redirect('overview:overview')

    return redirect('projects:lesson', project_id=project_id, lesson_id=lesson_id, chapter_id=next_chapter_id)


