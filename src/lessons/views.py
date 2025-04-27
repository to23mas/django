"""views.py"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.blockly.BlocklyStorage import BlocklyStorage
from lessons.enum.UnknownChapterId import UnknownChapterId
from domain.data.chapters.ChapterStorage import ChapterStorage
from domain.data.lessons.LessonStorage import LessonStorage
from domain.data.progress.ProgressStorage import ProgressStorage
from domain.data.projects.ProjectStorage import ProjectStorage
from domain.data.tests_progress.TestProgressStorage import TestProgressStorage
from domain.data.clis.CliStorage import CliStorage


@login_required
def lesson(request: HttpRequest, course: str, project_id: int, lesson_id: int, chapter_id: int) -> HttpResponse:
	"""display chapter"""
	username = request.user.username #type: ignore
	project = ProjectStorage().get_project_by_id(project_id, course)
	if project is None:
		messages.error(request, 'pokus o vstup k neexistujícímu projektu!')
		return redirect('projects:overview', course=course, sort_type='all')

	lesson_data = LessonStorage().get_lesson(lesson_id, course, project.database)
	if lesson_data is None:
		messages.error(request, 'Pokus o vstup k neexistující lekci!')
		return redirect('projects:overview', course=course, sort_type='all')

	lesson_progress = ProgressStorage().get_content_progress(course, username, 'lessons')
	if lesson_progress[str(lesson_id)] == "lock":
		messages.warning(request, 'Lekce ještě není odemčena!')
		return redirect('projects:overview', course=course, sort_type='all')

	if chapter_id == UnknownChapterId.ID.value:
		chapters = ChapterStorage().find_chapters(course, project.database, {'lesson_id': lesson_data.id})
		if chapters is None:
			chapter = None
		else:
			chapter = chapters[0] #pylint: disable=E1136

	else:
		chapter = ChapterStorage().get_chapter(chapter_id, lesson_id, course , project.database)
	if chapter is None:
		messages.error(request, 'Pokus o vstup k neexistující kapitole!')
		return redirect('projects:overview', course=course, sort_type='all')

	chapter_progress = ProgressStorage().get_content_progress(course, username, 'chapters')
	if chapter_progress[str(project_id)][str(chapter.id)] == 'lock':
		messages.warning(request, 'Kapitola ještě není odemčena!')
		return redirect('projects:overview', course=course, sort_type='all')

	if chapter.unlock_type == 'blockly':
		blockly = BlocklyStorage().get_blockly(course, chapter.unlocker_id) #type: ignore
	else: blockly = None

	if chapter.unlock_type == 'cli':
		cli = CliStorage().get_cli(course, chapter.unlocker_id) #type: ignore
	else: cli = None

	test_state = None
	if chapter.unlock_type == 'test':
		test = TestProgressStorage().get_test_progress(course, username, chapter.unlocker_id)
		if test is not None:
			test_state = test.state


	is_last_chapter = False
	next_chapter_data = ChapterStorage().get_chapter_by_id(chapter.unlock_id, course, project.database)
	if next_chapter_data is None:
		is_last_chapter = True

	lesson_chapters = ChapterStorage().find_chapters(course, project.database, {"lesson_id": lesson_id})
	return render(request, 'lessons/lesson.html', {
		'blockly': blockly,
		'cli': cli,
		'project_id': project_id,
		'lesson': lesson,
		'project': project,
		'lesson_chapters': lesson_chapters,
		'chapter': chapter,
		'chapter_finished': chapter_progress[str(project_id)][str(chapter.id)] == 'done',
		'sidebar_progress': chapter_progress,
		'chapter_id': chapter_id,
		'course': course,
		'username': username,
		'test_state': test_state,
		'is_last_chapter': is_last_chapter,
	})
