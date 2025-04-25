from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from domain.data.demos.DemoStorage import DemoStorage
from domain.data.progress.ProgressStorage import ProgressStorage

def check_demo_access(request: HttpRequest, course: str, demo_id: int):
	username = request.user.username #type: ignore
	if (ProgressStorage().get_user_progress_by_course(username, course) is None):
		messages.warning(request, 'Kurz ještě není odemčen!')
		return None, None, None, redirect('courses:overview')

	demo = DemoStorage().get_demo(demo_id, course)
	if demo is None:
		messages.warning(request, 'Ukázkový projekt není v tyto chvíli dostupný')
		return None, None, None, redirect('courses:overview')

	user_available_project_id = ProgressStorage().find_available_demos(course, username)
	user_available_demos = DemoStorage().find_demos(course)
	if user_available_demos is None or demo.project_id not in user_available_project_id:
		messages.warning(request, 'Ukázkový projekt ještě není odemčen')
		return None, None, None, redirect('courses:overview')

	project_url = reverse('projects:detail', kwargs={'course': course, 'project_id': demo.project_id})

	return username, demo, course, project_url 