from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from domain.data.demos.DemoStorage import DemoStorage
from domain.data.progress.ProgressStorage import ProgressStorage
from domain.data.projects.ProjectStorage import ProjectStorage


@login_required
def login(request: HttpRequest, course: str, demo_id: int) -> HttpResponse:
	username = request.user.username #type: ignore
	if (ProgressStorage().get_user_progress_by_course(username, course) is None):
		messages.warning(request, 'Kurz ještě není odemčen!')
		return redirect('courses:overview')

	demo = DemoStorage().get_demo(demo_id, course)
	if demo is None:
		messages.warning(request, 'Ukázkový projekt není v tyto chvíli dostupný')
		return redirect('courses:overview', course=course)
	#
	# user_available = ProgressStorage().find_available_demos(course, username)
	# if user_available is None or demo.id not in user_available:
	# 	messages.warning(request, 'Ukázkový projekt ještě není odemčen')
	# 	return redirect('courses:overview', course=course)
	#
	# project = ProjectStorage().get_project_by_id(demo_id, course)
	# if project is None:
	# 	messages.error(request, 'nevalidní akce')
	# 	return redirect('courses:overview', course=course)

	# project_url = reverse('projects:detail', kwargs={'course': course, 'project_id': project.id})
	project_url = reverse('projects:detail', kwargs={'course': course, 'project_id': 1})
	return render(request, 'demos/demo/login.html', {
		'demo': demo,
		'username': username,
		'course': course,
		'project_url': project_url,
})
