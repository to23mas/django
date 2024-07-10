from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.content_progress.ContentProgressStorage import get_content_progress
from domain.data.progress_storage import get_lesson_progress, get_user_progress_by_course
from domain.data.projects.ProjectStorage import find_projects_by_course, find_projects_by_course_and_ids, get_project


@login_required
def overview(request: HttpRequest, course: str, sort_type: str) -> HttpResponse:
	"""list all projects"""

	username = request.user.username #type: ignore

	if sort_type == 'all':
		projects_collection = find_projects_by_course(course)
	else:
		project_progress = get_content_progress(course, username, 'projects')
		filtered_project_ids = [int(key) for key, value in project_progress.items() if value == sort_type]
		projects_collection = find_projects_by_course_and_ids(filtered_project_ids, course)

	if not projects_collection:
		messages.warning(request, 'V tomto kurzu nebyly nalezeny žádné projekty.')

	return render(request, 'projects/overview.html', {
		'projects': projects_collection,
		'course_name': course,
		'username': username
	})


@login_required
def detail(request: HttpRequest, course: str, project_no: int) -> HttpResponse:
	"""detail view for projects"""

	username = request.user.username #type: ignore
	project_progress = get_content_progress(course, username, 'projects')
	project, lessons_graph_data = get_project(project_no, course)

	# non exissting project
	if project == None or lessons_graph_data == None:
		messages.error(request, 'Pokus o vstup do neexistujícího projektu!')
		return redirect('projects:overview', course=course, sort_type='all')

	# locked project
	if project_progress[str(project_no)] == 'lock':
		messages.warning(request, 'Projekt ještě není odemčen!')
		return redirect('projects:overview', course=course, sort_type='all')

	# need this to build the lesson graph
	lessons_progress = get_content_progress(course, username, 'lessons')
	print(lessons_progress)
	return render(request, 'projects/detail.html', {
		'project': project,
		'lessons_graph_data': lessons_graph_data,
		'lessons_progress': lessons_progress,
		'course_name': course,
	})
