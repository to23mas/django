from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from domain.data.demos.DemoStorage import get_demo
from domain.data.progress.ProgressStorage import find_available_demos, get_user_progress_by_course


@login_required
def hello_world(request: HttpRequest, course: str, demo_id: int) -> HttpResponse:
	username = request.user.username #type: ignore
	if (get_user_progress_by_course(username, course) == None):
		messages.warning(request, 'Kurz ještě není odemčen!')
		return redirect('courses:overview')

	demo = get_demo(demo_id, course)
	if demo == None:
		messages.warning(request, 'Ukázkový projekt není v tyto chvíli dostupný')
		return redirect('courses:overview', course=course)

	user_available = find_available_demos(course, username)

	if user_available == None or not demo.id in user_available:
		messages.warning(request, 'Ukázkový projekt ještě není odemčen')
		return redirect('courses:overview', course=course)

	return render(request, 'demos/demo/hello_world.html', {
		'demo': demo,
		'username': username,
		'course': course,
	})

