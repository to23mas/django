"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.chapters_storage import chapter_is_accessible_and_done, get_chapter, is_chapter_open, is_chapter_open_or_done
from domain.data.progress_storage import finish_chapter, unlock_chapter


@login_required
def next_chapter(request: HttpRequest) -> HttpResponse:
    """display lesson"""

    username = request.user.username #type: ignore
    if request.method != 'POST':
        pass # TODO redirect to overview/kurzy

    chapter_no = request.POST.get('chapter_no')
    lesson_no = request.POST.get('lesson_no')
    project_no = request.POST.get('project_no')
    course = request.POST.get('course')

    if not chapter_is_accessible_and_done(username, course, project_no, lesson_no, chapter_no): #type: ignore
        messages.warning(request, 'Nevalidní akce')
        return redirect('projects:overview', course=course, sort_type='all')

    next_chapter = int(chapter_no) + 1 #type: ignore
    if not is_chapter_open_or_done(username, course, project_no, lesson_no, str(next_chapter)): #type: ignore
        messages.warning(request, 'Pokus o přístup k zamčené kapitole')
        return redirect('projects:overview', course=course, sort_type='all')

    if (get_chapter(project_no, lesson_no, next_chapter, course) == None):
        # check if next chapter exists
        pass # TODO -> redirect na další lekci nebo na seznam lekcí bude asi jednoduší

    return redirect('projects:lesson', course=course, project_no=project_no, lesson_no=lesson_no, chapter_no=next_chapter)


@login_required
def unlock_next_chapter(request: HttpRequest) -> HttpResponse:
    """unlock chapter and redirect there"""

    username = request.user.username #type: ignore

    if request.method != 'POST':
        pass # TODO redirect to overview/kurzy

    chapter_no = request.POST.get('chapter_no')
    lesson_no = request.POST.get('lesson_no')
    project_no = request.POST.get('project_no')
    course = request.POST.get('course')
    next_chapter = int(chapter_no) + 1 #type: ignore

    if not is_chapter_open(username, course, project_no, lesson_no, chapter_no): #type: ignore
        # pravděpodobně podvržený formulář (uživatel posílá akci z místa kde ve skutečnosti být nemůže
        messages.warning(request, 'Nevalidní akce')
        return redirect('projects:overview', course=course, sort_type='all')

    if (get_chapter(project_no, lesson_no, str(next_chapter), course) == None):
        # does next chapter extist redirect to unlock lesson
        messages.error(request, 'jednalo se o poslední kapitolu v lekci')
        return redirect('projects:overview', course=course, sort_type='all')


    finish_chapter(username, course, lesson_no, chapter_no)
    unlock_chapter(username, course, lesson_no, next_chapter)

    return redirect('projects:lesson', course=course, project_no=project_no, lesson_no=lesson_no, chapter_no=next_chapter)
