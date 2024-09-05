from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from domain.data.demos.DemoStorage import find_demos_for_overview, get_demo
from domain.data.progress.ProgressStorage import find_available_demos, get_user_progress_by_course


@login_required
def overview(request: HttpRequest, course: str) -> HttpResponse:
	"""list of all available demos"""
	username = request.user.username #type: ignore
    # TODO přidat tenhle check na více míst (lekce , teste apod)
	if (get_user_progress_by_course(username, course) == None):
		messages.warning(request, 'Kurz ještě není odemčen!')
		return redirect('courses:overview')

	user_available = find_available_demos(course, username)

	if user_available == None or len(user_available) == 0:
		messages.success(request, 'V tuto chvíli nemáš žádné dostupné ukázky projektů')
		return render(request, 'demos/overview.html', {
			'course': course,
		})

	available_demos = find_demos_for_overview(course, user_available)

	return render(request, 'demos/overview.html', {
		'demos': available_demos,
		'username': username,
		'course': course,
	})


@login_required
def detail(request: HttpRequest, course: str, demo_id: int) -> HttpResponse:
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

	return redirect(f'demos:{demo.url}', course=course, demo_id=demo.id)
