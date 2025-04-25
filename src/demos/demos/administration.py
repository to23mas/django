from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from ..utils import check_demo_access


@login_required
def administration(request: HttpRequest, course: str, demo_id: int) -> HttpResponse:
	username, demo, course, project_url = check_demo_access(request, course, demo_id)
	if isinstance(project_url, HttpResponse):
		return project_url

	return render(request, 'demos/demo/administration.html', {
		'demo': demo,
		'username': username,
		'course': course,
		'project_url': project_url,
	})
