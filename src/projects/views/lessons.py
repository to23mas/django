"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.chapters.ChapterStorage import find_chapters, get_chapter
from domain.data.content_progress.ContentProgressStorage import get_content_progress
from domain.data.lessons.LessonStorage import get_lesson
from domain.data.projects.ProjectStorage import get_project_by_id


@login_required
def lesson(request: HttpRequest, course: str, project_id: int, lesson_id: int, chapter_id: int) -> HttpResponse:
	"""display lesson"""
	username = request.user.username #type: ignore
	project = get_project_by_id(project_id, course)
	if project == None:
		messages.error(request, 'pokus o vstup k neexistujícímu projektu!')
		return redirect('projects:overview', course=course, sort_type='all')

	lesson = get_lesson(lesson_id, course, project.database)
	if lesson == None:
		messages.error(request, 'Pokus o vstup k neexistující lekci!')
		return redirect('projects:overview', course=course, sort_type='all')

	lesson_progress = get_content_progress(course, username, 'lessons')
	if lesson_progress[str(lesson_id)] == "lock":
		messages.warning(request, 'Lekce ještě není odemčena!')
		return redirect('projects:overview', course=course, sort_type='all')

	chapter = get_chapter(chapter_id, lesson_id, course , project.database)
	if chapter == None:
		messages.error(request, 'Pokus o vstup k neexistující kapitole!')
		return redirect('projects:overview', course=course, sort_type='all')

	chapter_progress = get_content_progress(course, username, 'chapters')
	if chapter_progress[str(chapter_id)] == 'lock':
		messages.warning(request, 'Kapitola ještě není odemčena!')
		return redirect('projects:overview', course=course, sort_type='all')

	lesson_chapters = find_chapters(course, project.database, {"lesson_id": lesson_id})
	return render(request, 'projects/lesson.html', {
		'project_id': project_id,
		'lesson': lesson,
		'lesson_chapters': lesson_chapters,
		'chapter': chapter,
		'chapter_finished': chapter_progress[str(chapter_id)] == 'done',
		'sidebar_progress': chapter_progress,
		# 'sidebar_progress': progress['chapters'][str(lesson_no)],
		'chapter_id': chapter_id,
		'course_name': course,
		'username': username,
	})

