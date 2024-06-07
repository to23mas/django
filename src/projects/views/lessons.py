"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from domain.data.projects_storage import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def lesson(request: HttpRequest, course: str, project_no: int, lesson_no: int, chapter_no: int) -> HttpResponse:
    """display lesson"""

    lesson = get_lesson(lesson_no, course)
    chapter = get_chapter(chapter_no, course)

    # non existing lesson or chapter
    if lesson == None or chapter == None:
        messages.error(request, 'Pokus o vstup k neexistujícím zdrojům!')
        return redirect('projects:overview', course=course, sort_type='all')

    # locked lesson or chapter
    progress = get_progress_projects(request.user.username, course) #type: ignore
    if lesson_no in progress['lessons'][str(project_no)]['lock'] or chapter_no in progress['chapters'][str(lesson_no)]['lock']: #type: ignore
        messages.warning(request, 'Lekce/kapitola ještě není odemčena!')
        return redirect('projects:overview', course=course, sort_type='all')

    return render(request, 'projects/lesson.html', {
        'project_no': project_no,
        'lesson': lesson,
        'chapter': chapter,
        'chapter_finished': chapter_no in progress['chapters'][str(lesson_no)]['done'], #type: ignore
        'sidebar_progress': progress['chapters'][str(lesson_no)], #type: ignore
        'chapter_no': chapter_no,
        'course_name': course,
    })

