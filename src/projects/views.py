"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from domain.data.projects_storage import *
from django.contrib.auth.decorators import login_required


@login_required
def project_detail(request: HttpRequest, project_id: int) -> HttpResponse:
    """detail view for projets"""

    return render(request, 'project_detail.html', {
        'project': get_project_detail(project_id),
    })

@login_required
def lesson(request: HttpRequest, lesson_id: int, chapter_id: int) -> HttpResponse:
    """display lesson"""

    return render(request, 'lesson.html', {
        'lesson': get_lesson(lesson_id),
        'chapter': get_chapter(chapter_id),
        'chapter_id': chapter_id,
    })
