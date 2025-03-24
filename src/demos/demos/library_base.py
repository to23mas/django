from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from django.urls import reverse
from domain.data.demos.DemoStorage import DemoStorage
from domain.data.progress.ProgressStorage import ProgressStorage

def _check(request: HttpRequest, course: str, demo_id: int):
	username = request.user.username #type: ignore
	if (ProgressStorage().get_user_progress_by_course(username, course) is None):
		messages.warning(request, 'Kurz ještě není odemčen!')
		return redirect('courses:overview')

	demo = DemoStorage().get_demo(demo_id, course)
	if demo is None:
		messages.warning(request, 'Ukázkový projekt není v tyto chvíli dostupný')
		return redirect('courses:overview')

	project_url = reverse('projects:detail', kwargs={'course': course, 'project_id': demo_id})
	return username, demo, course, project_url

def library(request: HttpRequest, course: str, demo_id: int):
	result = _check(request, course, demo_id)
	if hasattr(result, 'url'):
		return result
	username, demo, course, project_url = result

	return render(request, 'demos/demo/library_iframe_parent.html', {
		'demo': demo,
		'course': course,
		'username': username,
		'project_url': project_url
	})

def library_iframe(request: HttpRequest, course: str, demo_id: int):
	result = _check(request, course, demo_id)
	if hasattr(result, 'url'):
		return result
	username, demo, course, project_url = result

	return render(request, 'demos/demo/library_iframe.html', {
		'demo': demo,
		'course': course,
		'username': username,
		'project_url': project_url
	})

def library_rest_view(request: HttpRequest, course: str, demo_id: int):
	result = _check(request, course, demo_id)
	if hasattr(result, 'url'):
		return result
	username, demo, course, project_url = result

	return render(request, 'demos/demo/library_rest.html', {
		'demo': demo,
		'course': course,
		'username': username,
		'project_url': project_url
	})

def library_graphql(request: HttpRequest, course: str, demo_id: int):
	result = _check(request, course, demo_id)
	if hasattr(result, 'url'):
		return result
	username, demo, course, project_url = result

	return render(request, 'demos/demo/library_graphql.html', {
		'demo': demo,
		'course': course,
		'username': username,
		'project_url': project_url
	})
