"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.chapters_storage import get_chapter
from domain.data.content_progress.ContentProgressStorage import get_content_progress
from domain.data.lessons.LessonStorage import get_lesson


@login_required
def lesson(request: HttpRequest, course: str, project_no: str, lesson_no: str, chapter_no: str) -> HttpResponse:
	"""display lesson"""

	#TODO fix progress because of the data refactor
	username = request.user.username #type: ignore

	lesson = get_lesson(lesson_no, project_no, course)
	if lesson == None:
		messages.error(request, 'Pokus o vstup k neexistující lekci!')
		return redirect('projects:overview', course=course, sort_type='all')

	lesson_progress = get_content_progress(course, username, 'lessons')
	if lesson_progress[str(lesson_no)] == "lock":
		messages.warning(request, 'Lekce ještě není odemčena!')
		return redirect('projects:overview', course=course, sort_type='all')

	chapter = get_chapter(project_no, lesson_no, chapter_no, course)
	if chapter == None:
		messages.error(request, 'Pokus o vstup k neexistující kapitole!')
		return redirect('projects:overview', course=course, sort_type='all')

	chapter_progress = get_content_progress(course, username, 'chapters')
	if chapter_progress[str(chapter_no)] == 'lock':
		messages.warning(request, 'Kapitola ještě není odemčena!')
		return redirect('projects:overview', course=course, sort_type='all')

	return render(request, 'projects/lesson.html', {
		'project_no': project_no,
		'lesson': lesson,
		'chapter': chapter,
		'chapter_finished':chapter_progress[str(chapter_no)] == 'done',
		'sidebar_progress': chapter_progress,
		# 'sidebar_progress': progress['chapters'][str(lesson_no)],
		'chapter_no': chapter_no,
		'course_name': course,
	})

