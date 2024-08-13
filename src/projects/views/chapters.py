"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.chapters.ChapterStorage import get_chapter, get_chapter_by_id
from domain.data.progress.ProgressStorage import finish_chapter, finish_lesson, is_chapter_open, unlock_chapter, chapter_is_accessible_and_done, unlock_lesson
from domain.data.projects.ProjectStorage import get_project_by_id


@login_required
def next_chapter(request: HttpRequest):
# def next_chapter(request: HttpRequest) -> HttpResponse:
	"""display lesson"""
	username = request.user.username #type: ignore

	if request.method != 'POST':
		pass # TODO redirect to overview/kurzy

	chapter_id = int(request.POST.get('chapter_id'))
	lesson_id = int(request.POST.get('lesson_id'))
	project_id = int(request.POST.get('project_id'))
	course = request.POST.get('course')


	# TODO go to next chapter
	print(chapter_is_accessible_and_done(username, str(course), project_id, lesson_id, chapter_id))
    #     messages.warning(request, 'Nevalidní akce')
    #     return redirect('projects:overview', course=course, sort_type='all')
    #
    # next_chapter = int(chapter_no) + 1 #type: ignore
    # if not is_chapter_open_or_done(username, course, project_no, lesson_no, str(next_chapter)): #type: ignore
    #     messages.warning(request, 'Pokus o přístup k zamčené kapitole')
    #     return redirect('projects:overview', course=course, sort_type='all')
    #
    # if (get_chapter(project_no, lesson_no, next_chapter, course) == None):
    #     # check if next chapter exists
    #     pass # TODO -> redirect na další lekci nebo na seznam lekcí bude asi jednoduší
    #
    # return redirect('projects:lesson', course=course, project_no=project_no, lesson_no=lesson_no, chapter_no=next_chapter)


@login_required
def unlock_next_chapter(request: HttpRequest) :
# def unlock_next_chapter(request: HttpRequest) -> HttpResponse:
	"""unlock chapter and redirect there"""
	username = request.user.username #type: ignore

	chapter_id = int(str(request.POST.get('chapter_id')))
	lesson_id = int(str(request.POST.get('lesson_id')))
	project_id = int(str(request.POST.get('project_id')))
	course_db = str(request.POST.get('course'))

	if request.method != 'POST':
		return redirect('projects:overview', course=course_db, sort_type='all')

	project = get_project_by_id(project_id, course_db)
	if project == None: return redirect('projects:overview', course=course_db, sort_type='all')
	chapter = get_chapter(chapter_id, lesson_id, course_db, project.database)
	if chapter == None: return redirect('projects:overview', course=course_db, sort_type='all')


	if not is_chapter_open(username, course_db, project_id, lesson_id, chapter_id): #type: ignore
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
		return redirect('projects:overview', course=course_db, sort_type='all')


	finish_chapter(username, course_db, chapter.id)
	unlock_chapter(username, course_db, chapter.unlock_id)
	messages.success(request, 'Kapitola ůspěšně splněna.')
	return redirect('projects:lesson', course=course_db, project_id=project_id, lesson_id=next_chapter.lesson_id, chapter_id=next_chapter.id)
