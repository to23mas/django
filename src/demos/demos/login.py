from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from domain.data.demos.DemoStorage import DemoStorage
from domain.data.progress.ProgressStorage import ProgressStorage


@login_required
def login(request: HttpRequest, course: str, demo_id: int) -> HttpResponse:
	username = request.user.username #type: ignore
	if (ProgressStorage().get_user_progress_by_course(username, course) is None):
		messages.warning(request, 'Kurz ještě není odemčen!')
		return redirect('courses:overview')

	demo = DemoStorage().get_demo(demo_id, course)
	if demo is None:
		messages.warning(request, 'Ukázkový projekt není v tyto chvíli dostupný')
		return redirect('courses:overview')

	user_available_project_id = ProgressStorage().find_available_demos(course, username)
	user_available_demos = DemoStorage().find_demos(course)
	if user_available_demos is None or demo.project_id not in user_available_project_id:
		messages.warning(request, 'Ukázkový projekt ještě není odemčen')
		return redirect('courses:overview')

	project_url = reverse('projects:detail', kwargs={'course': course, 'project_id': demo.project_id})

	return render(request, 'demos/demo/login.html', {
		'demo': demo,
		'username': username,
		'course': course,
		'project_url': project_url,
})
