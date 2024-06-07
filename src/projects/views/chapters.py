"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from domain.data.projects_storage import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def next_chapter(request: HttpRequest) -> HttpResponse:
    """display lesson"""

    if request.method != 'POST':
        pass

    chapter_no = request.POST.get('chapter_no')
    lesson_no = request.POST.get('lesson_no')
    project_no = request.POST.get('project_no')
    course = request.POST.get('course')

    if not chapter_is_accessible_and_done(request.user.username, course, project_no, lesson_no, chapter_no): #type: ignore
        messages.warning(request, 'Nevalidní akce')
        return redirect('projects:overview', course=course, sort_type='all')

    next_chapter = int(chapter_no) + 1 #type: ignore
    if not is_chapter_open(request.user.username, course, project_no, lesson_no, str(next_chapter)): #type: ignore
        messages.warning(request, 'Pokus o přístup k zamčené kapitole')
        return redirect('projects:overview', course=course, sort_type='all')

    if (get_chapter(next_chapter, course) == None): #type: ignore
        pass # TODO -> redirect na další lekci nebo na seznam lekcí bude asi jednoduší

    return redirect('projects:lesson', course=course, project_no=project_no, lesson_no=lesson_no, chapter_no=next_chapter)


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



