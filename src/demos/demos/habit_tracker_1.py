import json
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from domain.data.demos.DemoStorage import DemoStorage
from domain.data.progress.ProgressStorage import ProgressStorage
from domain.data.projects.ProjectStorage import ProjectStorage

def _check(request: HttpRequest, course: str, demo_id: int):
	username = request.user.username #type: ignore
	if (ProgressStorage().get_user_progress_by_course(username, course) is None):
		messages.warning(request, 'Kurz ještě není odemčen!')
		return redirect('courses:overview')

	demo = DemoStorage().get_demo(demo_id, course)
	if demo is None:
		messages.warning(request, 'Ukázkový projekt není v tyto chvíli dostupný')
		return redirect('courses:overview', course=course)

	# TODO uncomment when project is ready
	# user_available = ProgressStorage().find_available_demos(course, username)
	# if user_available is None or demo.id not in user_available:
	# 	messages.warning(request, 'Ukázkový projekt ještě není odemčen')
	# 	return redirect('courses:overview', course=course)

	# project = ProjectStorage().get_project_by_id(demo_id, course)
	# if project is None:
	# 	messages.error(request, 'nevalidní akce')
	# 	return redirect('courses:overview', course=course)

	# project_url = reverse('projects:detail', kwargs={'course': course, 'project_id': project.id})
	project_url = reverse('projects:detail', kwargs={'course': course, 'project_id': 1})

	return username, demo, course, project_url

@login_required
def h_t_1(request: HttpRequest, course: str, demo_id: int):
	username, demo, course, project_url = _check(request, course, demo_id)
	return render(request, 'demos/demo/habit_tracker_1.html', {
		'demo': demo,
		'username': username,
		'course': course,
		'project_url': project_url,
	})

def habit_tracker_1(request: HttpRequest, course: str, demo_id: int):
	username, demo, course, project_url = _check(request, course, demo_id)

	if 'habits' not in request.session:
		request.session['habits'] = json.dumps([
			{'name': 'Pít vodu', 'completed': True, 'completion_count': 5},
			{'name': 'Cvičit', 'completed': False, 'completion_count': 1},
			{'name': 'Číst knihu', 'completed': False, 'completion_count': 0}
		])
		request.session.modified = True

	habits = json.loads(request.session.get('habits', '[]'))

	if request.method == "POST":
		habit_name = request.POST.get("habit_name")
		if habit_name:
			habits = json.loads(request.session.get('habits', '[]'))

			if habit_name not in [habit['name'] for habit in habits]:
				habits.append({'name': habit_name, 'completed': False, 'completion_count': 0})

			request.session['habits'] = json.dumps(habits)
			request.session.modified = True

			return redirect('demos:habit_tracker_1', course=course, demo_id=demo_id)

	return render(request, 'demos/demo/habit_tracker_1_iframe.html', {
		'demo': demo,
		'username': username,
		'course': course,
		'project_url': project_url,
		'habits': habits,
	})

def complete_habit_1(request: HttpRequest, course: str, demo_id: int, habit_name):
	_, _, course, _ = _check(request, course, demo_id)
	habits = json.loads(request.session.get('habits', '[]'))
	completed_habits = json.loads(request.session.get('completed_habits', '[]'))

	for habit in habits:
		if habit['name'] == habit_name and habit_name not in completed_habits:
			habit['completed'] = True
			habit['completion_count'] += 1

	request.session['habits'] = json.dumps(habits)
	request.session.modified = True

	completed_habits.append(habit_name)
	request.session['completed_habits'] = json.dumps(completed_habits)
	request.session.modified = True

	return redirect('demos:h_t_1', course=course, demo_id=demo_id)


def delete_habit_1(request: HttpRequest, course: str, demo_id: int, habit_name):
	_, _, course, _ = _check(request, course, demo_id)
	habits = json.loads(request.session.get('habits', '[]'))
	completed_habits = json.loads(request.session.get('completed_habits', '[]'))

	habits = [habit for habit in habits if habit['name'] != habit_name]
	request.session['habits'] = json.dumps(habits)
	request.session.modified = True

	if habit_name in completed_habits:
		completed_habits.remove(habit_name)
		request.session['completed_habits'] = json.dumps(completed_habits)
		request.session.modified = True

	return redirect('demos:h_t_1', course=course, demo_id=demo_id)

def clear_session_1(request: HttpRequest, course: str, demo_id: int):
	try:
		del request.session['habits']
		del request.session['completed_habits']
	except KeyError:
		pass

	return redirect('demos:h_t_1', course=course, demo_id=demo_id)

