from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from ..utils import check_demo_access

def library_base(request: HttpRequest, course: str, demo_id: int):
	username, demo, course, project_url = check_demo_access(request, course, demo_id)
	if isinstance(project_url, HttpResponse):
		return project_url

	return render(request, 'demos/demo/library_iframe_parent.html', {
		'demo': demo,
		'course': course,
		'username': username,
		'project_url': project_url
	})

def library_iframe(request: HttpRequest, course: str, demo_id: int):
	username, demo, course, project_url = check_demo_access(request, course, demo_id)
	if isinstance(project_url, HttpResponse):
		return project_url

	return render(request, 'demos/demo/library_iframe.html', {
		'demo': demo,
		'course': course,
		'username': username,
		'project_url': project_url
	})

def library_rest_view(request: HttpRequest, course: str, demo_id: int):
	username, demo, course, project_url = check_demo_access(request, course, demo_id)
	if isinstance(project_url, HttpResponse):
		return project_url

	return render(request, 'demos/demo/library_rest.html', {
		'demo': demo,
		'course': course,
		'username': username,
		'project_url': project_url
	})

def library_graphql(request: HttpRequest, course: str, demo_id: int):
	username, demo, course, project_url = check_demo_access(request, course, demo_id)
	if isinstance(project_url, HttpResponse):
		return project_url

	return render(request, 'demos/demo/library_graphql.html', {
		'demo': demo,
		'course': course,
		'username': username,
		'project_url': project_url
	})
