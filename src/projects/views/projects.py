from typing import Dict, List
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.chapters.ChapterData import ChapterData
from domain.data.chapters.ChapterStorage import find_chapters
from domain.data.content_progress.ContentProgressStorage import get_content_progress
from domain.data.demos.DemoStorage import get_demo
from domain.data.lessons.LessonData import LessonData
from domain.data.lessons.LessonStorage import find_lessons
from domain.data.progress.ProgressStorage import get_user_progress_by_course
from domain.data.projects.ProjectData import ProjectData
from domain.data.projects.ProjectStorage import find_projects, find_projects_by_course_and_ids, get_project_by_id


@login_required
def overview(request: HttpRequest, course: str, sort_type: str) -> HttpResponse:
	"""list all projects"""
	username = request.user.username #type: ignore

	if sort_type == 'all':
		projects_collection = find_projects(course)
	else:
		project_progress = get_content_progress(course, username, 'projects')
		filtered_project_ids = [int(key) for key, value in project_progress.items() if value == sort_type]
		projects_collection = find_projects_by_course_and_ids(filtered_project_ids, course)

	if not projects_collection:
		messages.warning(request, 'V tomto kurzu nebyly nalezeny žádné projekty.')

	return render(request, 'projects/overview.html', {
		'projects': projects_collection,
		'course': course,
		'username': username
	})


@login_required
def detail(request: HttpRequest, course: str, project_id: int) -> HttpResponse:
	"""detail view for projects"""
	username = request.user.username #type: ignore
	project_progress = get_content_progress(course, username, 'projects')
	project = get_project_by_id(project_id, course)

	# non existing project
	if project == None:
		messages.error(request, 'Pokus o vstup do neexistujícího projektu!')
		return redirect('projects:overview', course=course, sort_type='all')

	# locked project
	if project_progress[str(project_id)] == 'lock':
		messages.warning(request, 'Projekt ještě není odemčen!')
		return redirect('projects:overview', course=course, sort_type='all')

	user_progress = get_user_progress_by_course(username, course)
	chapters = find_chapters(course, project.database)
	lessons = find_lessons(course, project.database)
	ch, ch_edges = get_vis_chapters(chapters, user_progress, course, project)
	l, l_edges = get_vis_lessons(lessons, user_progress)

	demo_project = get_demo(project.id, course)
	match demo_project:
		case None: demo_url = None
		case _: demo_url = f'demos:{demo_project.url}'

	return render(request, 'projects/detail.html', {
		'project': project,
		'demo_url': demo_url,
		'lessons': lessons,
		'chapters': chapters,
		'course': course,
		'username': username,
		'ledges': l_edges,
		'chedges': ch_edges,
		'ch': ch,
		'l': l,
	})


def get_vis_lessons(lessons:  List[LessonData] | None, progress: Dict | None):
	ch = []
	edges = []
	if lessons == None or progress == None: return (None, None)
	for lesson in lessons:
		for to in lesson.to:
			edges.append({'from': lesson.id, 'to': to})

		lesson_status = progress['lessons'][str(lesson.id)]
		color = '#ffffff'
		match(lesson_status):
			case 'lock': color = '#cccccc'
			case 'done': color = '#34eb40'
			case 'open': color = '#34c6eb'

		ch.append({
			'id': lesson.id,
			'label': lesson.title,
			'color': color
		})

	return (ch, edges)


def get_vis_chapters(chapters: List[ChapterData] | None, progress: Dict | None, course: str, project: ProjectData):
	ch = []
	edges = []
	if chapters == None or progress == None: return (None, None)
	for chapter in chapters:
		edges.append({'from': f'c-{chapter.id}', 'to': chapter.lesson_id})
		chapter_status = progress['chapters'][str(chapter.id)]
		color = '#ffffff'
		match(chapter_status):
			case 'lock': color = '#cccccc'
			case 'done': color = '#34eb40'
			case 'open': color = '#34c6eb'

		match (chapter.unlock_type):
			case 'blockly': icon = ' 🧩'
			case 'test': icon = '🖊️'
			case _: icon = ' 📖'

		ch.append({
			'id': f'c-{chapter.id}',
			'chid': chapter.id,
			'lid': chapter.lesson_id,
			'label': f'{chapter.title} {icon}',
			'status': chapter_status,
			'url': '#' if chapter_status == 'lock' else reverse('projects:lesson', kwargs={
					'course': course,
					'project_id': project.id,
					'lesson_id': chapter.lesson_id,
					'chapter_id': chapter.id}),
			'color': color
		})

	return (ch, edges)

