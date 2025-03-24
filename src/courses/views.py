from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from domain.data.courses.CourseStorage import CourseStorage

from domain.data.progress.ProgressStorage import ProgressStorage


@login_required(login_url='/users/login/')
def overview(request: HttpRequest) -> HttpResponse:
	"""list all courses"""
	username = request.user.username #type: ignore

	return render(request, 'courses/overview.html', {
		'courses': CourseStorage().find_courses(),
		'courses_overview': True,
		'username': username,
	})


@login_required(login_url='/users/login/')
def enroll(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""

	username = request.user.username #type: ignore
	course = CourseStorage().get_course_by_id(course_id)
	if course is None: return  redirect('overview')

	if (ProgressStorage().enroll_course(username, course.database)):
		messages.success(request, 'Kurz byl zapsán')
	else:
		messages.error(request, 'Kurz nebylo možné zapsat')

	return redirect('courses:overview')
