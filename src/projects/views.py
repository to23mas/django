"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from domain.data.projects_storage import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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

    return render(request, 'project_detail.html', {
        'project': project
    })

@login_required
def lesson(request: HttpRequest, lesson_id: int, chapter_id: int) -> HttpResponse:
    """display lesson"""

    lesson = get_lesson(lesson_id)
    chapter = get_chapter(chapter_id)

    # non exissting lesson or chapter
    if lesson == None or chapter == None:
        messages.error(request, 'Pokus o vstup k neexistujícím zdrojům!')
        return redirect('overview:overview')

    # locked lesson or chapter
    progress = get_progress_projects(request.user.username)['projects'] #type: ignore
    if lesson_id in progress['lock'] or chapter_id in progress['lock']:
        messages.warning(request, 'Lekce/kapitola ještě není odemčena!')
        return redirect('overview:overview')

    return render(request, 'lesson.html', {
        'lesson': lesson,
        'chapter': chapter,
        'chapter_id': chapter_id,
    })
