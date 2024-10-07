from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from domain.data.demos.DemoStorage import get_demo
from domain.data.progress.ProgressStorage import find_available_demos, get_user_progress_by_course
from domain.data.projects.ProjectStorage import get_project_by_id


@login_required
def hello_world(request: HttpRequest, course: str, demo_id: int) -> HttpResponse:
	username = request.user.username #type: ignore
	if (get_user_progress_by_course(username, course) is None):
		messages.warning(request, 'Kurz ještě není odemčen!')
		return redirect('courses:overview')

	demo = get_demo(demo_id, course)
	if demo is None:
		messages.warning(request, 'Ukázkový projekt není v tyto chvíli dostupný')
		return redirect('courses:overview', course=course)

	user_available = find_available_demos(course, username)
	if user_available is None or demo.id not in user_available:
		messages.warning(request, 'Ukázkový projekt ještě není odemčen')
		return redirect('courses:overview', course=course)

	project = get_project_by_id(demo_id, course)
	if project is None:
		messages.error(request, 'nevalidní akce')
		return redirect('courses:overview', course=course)

	project_url = reverse('projects:detail', kwargs={'course': course, 'project_id': project.id})
	return render(request, 'demos/demo/hello_world.html', {
		'demo': demo,
		'username': username,
		'course': course,
		'project_url': project_url,
})
