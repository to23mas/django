"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.chapters.ChapterStorage import get_chapter, get_chapter_by_id
from domain.data.progress.ProgressStorage import finish_chapter, finish_lesson, is_chapter_done, is_chapter_open, is_chapter_open_or_done, unlock_chapter, unlock_lesson
from domain.data.projects.ProjectStorage import get_project_by_id


@login_required
def next_chapter(request: HttpRequest):
# def next_chapter(request: HttpRequest) -> HttpResponse:
	"""display lesson"""
	username = request.user.username #type: ignore

	if request.method != 'POST':
		return redirect('courses:overview')

	chapter_id = int(str(request.POST.get('chapter_id')))
	lesson_id = int(str(request.POST.get('lesson_id')))
	project_id = int(str(request.POST.get('project_id')))
	course_db = str(request.POST.get('course'))

	project = get_project_by_id(project_id, course_db)
	if project == None: return redirect('projects:overview', course=course_db, sort_type='all')
	chapter = get_chapter(chapter_id, lesson_id, course_db, project.database)
	if chapter == None: return redirect('projects:overview', course=course_db, sort_type='all')

	if not is_chapter_done(username, course_db, chapter.id):
		messages.warning(request, 'Nevalidní akce')
		return redirect('projects:overview', course=course_db, sort_type='all')

	next_chapter = get_chapter_by_id(chapter.unlock_id, course_db, project.database)
	if next_chapter == None:
		# TODO better redirect
		messages.warning(request, 'Jednalo se o poslední kapitolu projektu.')
		return redirect('projects:overview', course=course_db, sort_type='all')

	if not is_chapter_open_or_done(username, course_db, next_chapter.id):
		messages.warning(request, 'Pokus o přístup k zamčené kapitole')
		return redirect('projects:overview', course=course_db, sort_type='all')

	return redirect('projects:lesson', course=course_db, project_id=project.id, lesson_id=next_chapter.lesson_id, chapter_id=next_chapter.id)


@login_required
def unlock_next_chapter(request: HttpRequest) -> HttpResponse:
	"""unlock chapter and redirect there"""
	username = request.user.username #type: ignore

	chapter_id = int(str(request.POST.get('chapter_id')))
	lesson_id = int(str(request.POST.get('lesson_id')))
	project_id = int(str(request.POST.get('project_id')))
	course_db = str(request.POST.get('course'))
	# TODO check if the chapter unlock type is button (blockly and tests should have own methods)

	if request.method != 'POST':
		return redirect('courses:overview')

	project = get_project_by_id(project_id, course_db)
	if project == None: return redirect('projects:overview', course=course_db, sort_type='all')
	chapter = get_chapter(chapter_id, lesson_id, course_db, project.database)
	if chapter == None: return redirect('projects:overview', course=course_db, sort_type='all')

	if chapter.unlock_type != 'button':
		return redirect('projects:overview', course=course_db, sort_type='all')


	if not is_chapter_open(username, course_db, project_id, lesson_id, chapter_id): #type: ignore
		if (is_chapter_done(username, course_db, chapter.id)):
			messages.warning(request, 'Kapitola je již splněna')
			return redirect('projects:lesson', course=course_db, project_id=project_id, lesson_id=chapter.lesson_id, chapter_id=chapter.id)

		# pravděpodobně podvržený formulář (uživatel posílá akci z místa kde ve skutečnosti být nemůže
		messages.warning(request, 'Nevalidní akce')
		return redirect('projects:overview', course=course_db, sort_type='all')

	next_chapter = get_chapter_by_id(chapter.unlock_id, course_db, project.database)
	if next_chapter != None:
		unlock_lesson(username, course_db, chapter.unlock_id)
		if next_chapter.is_last:
			messages.success(request, 'Lekce ůspěšně splněna.')
			finish_lesson(username, course_db, chapter.lesson_id)
	else:
		finish_chapter(username, course_db, chapter.id)
		## probably unlock next project
		return redirect('projects:overview', course=course_db, sort_type='all')

	finish_chapter(username, course_db, chapter.id)
	unlock_chapter(username, course_db, chapter.unlock_id)
	messages.success(request, 'Kapitola ůspěšně splněna.')
	return redirect('projects:lesson', course=course_db, project_id=project_id, lesson_id=chapter.lesson_id, chapter_id=chapter.id)
