from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from domain.data.demos.DemoStorage import DemoStorage
from domain.data.progress.ProgressStorage import ProgressStorage


@login_required
def overview(request: HttpRequest, course: str) -> HttpResponse:
	"""list of all available demos"""
	username = request.user.username #type: ignore
	# (fixme) TODO přidat tenhle check na více míst (lekce , teste apod)

	user_progress = ProgressStorage().get_user_progress_by_course(username, course)
	if (user_progress is None):
		messages.warning(request, 'Kurz ještě není odemčen!')
		return redirect('courses:overview')

	available_demos_ids = []
	project_states = {}
	for project_id, project_state in user_progress['projects'].items():
		if (project_state != 'lock'):
			available_demos_ids.append(int(project_id))
			project_states[int(project_id)] = project_state

	if available_demos_ids is None or len(available_demos_ids) == 0:
		messages.success(request, 'V tuto chvíli nemáš žádné dostupné ukázky projektů')
		return render(request, 'demos/overview.html', {
			'course': course,
		})

	available_demos = DemoStorage().find_demos_for_overview(course, available_demos_ids)
	
	demos_with_states = []
	for demo in available_demos:
		demos_with_states.append({
			'demo': demo,
			'state': project_states.get(demo.project_id, 'open')
		})

	if (len(demos_with_states) == 0):
		messages.success(request, 'V tuto chvíli nemáš žádné dostupné ukázky projektů')

	return render(request, 'demos/overview.html', {
		'demos': demos_with_states,
		'username': username,
		'course': course,
	})


@login_required
def detail(request: HttpRequest, course: str, demo_id: int) -> HttpResponse:
	username = request.user.username #type: ignore
	if (ProgressStorage().get_user_progress_by_course(username, course) is None):
		messages.warning(request, 'Kurz ještě není odemčen!')
		return redirect('courses:overview')

	demo = DemoStorage().get_demo(demo_id, course)
	if demo is None:
		messages.warning(request, 'Ukázkový projekt není v tyto chvíli dostupný')
		return redirect('courses:overview', course=course)

	# TODO uncomment following
	user_available = ProgressStorage().find_available_demos(course, username)
	user_available = DemoStorage().find_demos(course)

	if user_available is None or demo.id not in user_available:
		messages.warning(request, 'Ukázkový projekt ještě není odemčen')
		return redirect('courses:overview', course=course)

	return redirect(f'demos:{demo.url}', course=course, demo_id=demo.id)
