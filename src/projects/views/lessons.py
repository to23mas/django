"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.chapters_storage import get_chapter
from domain.data.progress_storage import get_user_progress_by_course
from domain.data.lessons_storage import get_lesson


@login_required
def lesson(request: HttpRequest, course: str, project_no: str, lesson_no: str, chapter_no: str) -> HttpResponse:
    """display lesson"""

	#TODO fix progress because of the data refactor

    username = request.user.username #type: ignore

    lesson = get_lesson(lesson_no, project_no, course)
    if lesson == None:
        messages.error(request, 'Pokus o vstup k neexistující lekci!')
        return redirect('projects:overview', course=course, sort_type='all')


    chapter = get_chapter(project_no, lesson_no, chapter_no, course)
    if chapter == None:
        messages.error(request, 'Pokus o vstup k neexistující kapitole!')
        return redirect('projects:overview', course=course, sort_type='all')

    # locked lesson or chapter
    progress = get_user_progress_by_course(username, course)
    if progress == None or lesson_no in progress['lessons'][project_no]['lock']:
        messages.warning(request, 'Lekce ještě není odemčena!')
        return redirect('projects:overview', course=course, sort_type='all')

    if chapter_no in progress['chapters'][str(lesson_no)]['lock']:
        messages.warning(request, 'Kapitola ještě není odemčena!')
        return redirect('projects:overview', course=course, sort_type='all')

    return render(request, 'projects/lesson.html', {
        'project_no': project_no,
        'lesson': lesson,
        'chapter': chapter,
        'chapter_finished': chapter_no in progress['chapters'][str(lesson_no)]['done'],
        'sidebar_progress': progress['chapters'][str(lesson_no)],
        'chapter_no': chapter_no,
        'course_name': course,
    })

