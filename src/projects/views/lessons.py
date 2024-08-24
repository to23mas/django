"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.blockly.BlocklyStorage import get_blockly
from domain.data.chapters.ChapterStorage import find_chapters, get_chapter
from domain.data.content_progress.ContentProgressStorage import get_content_progress
from domain.data.lessons.LessonStorage import get_lesson
from domain.data.projects.ProjectStorage import get_project_by_id
from projects.views.enum.UnknownChapterId import UnknownChapterId


@login_required
def lesson(request: HttpRequest, course: str, project_id: int, lesson_id: int, chapter_id: int) -> HttpResponse:
	"""display lesson"""
	username = request.user.username #type: ignore
	project = get_project_by_id(project_id, course)
	messages.warning(request, 'Lekce ještě není odemčena!')
	messages.error(request, 'Lekce ještě není odemčena!')
	messages.success(request, 'Lekce ještě není odemčena!')
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

	if chapter_id == UnknownChapterId.ID.value:
		# vis js does not know what is the first chapter in lesson. Have to figure it out here
		chapters = find_chapters(course, project.database, {'lesson_id': lesson.id})
		if chapters == None:
			chapter = None
		else:
			chapter = chapters[0]

	else:
		chapter = get_chapter(chapter_id, lesson_id, course , project.database)
	if chapter == None:
		messages.error(request, 'Pokus o vstup k neexistující kapitole!')
		return redirect('projects:overview', course=course, sort_type='all')

	chapter_progress = get_content_progress(course, username, 'chapters')
	if chapter_progress[str(chapter.id)] == 'lock':
		messages.warning(request, 'Kapitola ještě není odemčena!')
		return redirect('projects:overview', course=course, sort_type='all')

	if chapter.unlock_type == 'blockly':
		blockly = get_blockly(course, chapter.unlocker_id) #type: ignore
	else: blockly = None

	lesson_chapters = find_chapters(course, project.database, {"lesson_id": lesson_id})
	return render(request, 'projects/lesson.html', {
		'blockly': blockly,
		'project_id': project_id,
		'lesson': lesson,
		'project': project,
		'lesson_chapters': lesson_chapters,
		'chapter': chapter,
		'chapter_finished': chapter_progress[str(chapter.id)] == 'done',
		'sidebar_progress': chapter_progress,
		'chapter_id': chapter_id,
		'course_name': course,
		'username': username,
	})

