"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.chapters.ChapterStorage import ChapterStorage
from domain.data.progress.ProgressStorage import ProgressStorage
from domain.data.projects.ProjectStorage import ProjectStorage


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

	project = ProjectStorage().get_project_by_id(project_id, course_db)
	if project is None: return redirect('projects:overview', course=course_db, sort_type='all')
	chapter = ChapterStorage().get_chapter(chapter_id, lesson_id, course_db, project.database)
	if chapter is None: return redirect('projects:overview', course=course_db, sort_type='all')

	if not ProgressStorage().is_chapter_done(username, course_db, chapter.id):
		messages.warning(request, 'Nevalidní akce')
		return redirect('projects:overview', course=course_db, sort_type='all')

	next_chapter_data = ChapterStorage().get_chapter_by_id(chapter.unlock_id, course_db, project.database)
	if next_chapter_data is None:
		messages.warning(request, 'Jednalo se o poslední kapitolu projektu.')
		return redirect('projects:overview', course=course_db, sort_type='all')

	if not ProgressStorage().is_chapter_open_or_done(username, course_db, next_chapter_data.id):
		messages.warning(request, 'Pokus o přístup k zamčené kapitole')
		return redirect('projects:overview', course=course_db, sort_type='all')

	return redirect('lessons:lesson', course=course_db, project_id=project.id, lesson_id=next_chapter_data.lesson_id, chapter_id=next_chapter_data.id)


@login_required
def unlock_next_chapter(request: HttpRequest) -> HttpResponse:
	"""unlock chapter and redirect there"""
	username = request.user.username #type: ignore

	chapter_id = int(str(request.POST.get('chapter_id')))
	lesson_id = int(str(request.POST.get('lesson_id')))
	project_id = int(str(request.POST.get('project_id')))
	course_db = str(request.POST.get('course'))

	# Validation part
	if request.method != 'POST':
		return redirect('courses:overview')

	project = ProjectStorage().get_project_by_id(project_id, course_db)
	if project is None: return redirect('projects:overview', course=course_db, sort_type='all')
	chapter = ChapterStorage().get_chapter(chapter_id, lesson_id, course_db, project.database)
	if chapter is None: return redirect('projects:overview', course=course_db, sort_type='all')

	if chapter.unlock_type != 'button':
		return redirect('projects:overview', course=course_db, sort_type='all')

	if not ProgressStorage().is_chapter_open(username, course_db, project_id, lesson_id, chapter_id): #type: ignore
		if (ProgressStorage().is_chapter_done(username, course_db, chapter.id)):
			messages.warning(request, 'Kapitola je již splněna')
			return redirect('lessons:lesson', course=course_db, project_id=project_id, lesson_id=chapter.lesson_id, chapter_id=chapter.id)

		# pravděpodobně podvržený formulář (uživatel posílá akci z místa kde ve skutečnosti být nemůže
		messages.warning(request, 'Nevalidní akce')
		return redirect('projects:overview', course=course_db, sort_type='all')


	# Unlock part
	next_chapter_data = ChapterStorage().get_chapter_by_id(chapter.unlock_id, course_db, project.database)
	if next_chapter_data is not None:
		ProgressStorage().unlock_lesson(username, course_db, next_chapter_data.lesson_id)
		ProgressStorage().unlock_chapter(username, course_db, next_chapter_data.id)

	ProgressStorage().finish_chapter(username, course_db, chapter.id)
	message =  'Kapitola ůspěšně splněna.'

	if chapter.is_last_in_lesson:
		message = 'Lekce ůspěšně splněna.'
		ProgressStorage().finish_lesson(username, course_db, chapter.lesson_id)

	if next_chapter_data is None:
		#last chapter in project
		# finish_project()
		# unlock_project()
		## probably unlock next project
		messages.warning(request, 'tak tady by mělo dojít ke splnění celého projektu, a odemčení dalšího')
		return redirect('projects:overview', course=course_db, sort_type='all')

	messages.success(request, message)
	return redirect('lessons:lesson', course=course_db, project_id=project_id, lesson_id=chapter.lesson_id, chapter_id=chapter.id)
