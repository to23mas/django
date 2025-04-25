from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from ..utils import check_demo_access


def chat(request: HttpRequest, course: str, demo_id: int):
	username, demo, course, project_url = check_demo_access(request, course, demo_id)
	if isinstance(project_url, HttpResponse):
		return project_url

	return render(request, "demos/demo/chat.html", {
		'room_name': username,
		'demo': demo,
		'username': username,
		'course': course,
		'project_url': project_url,
	})
