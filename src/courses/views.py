from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from domain.data.courses.CourseStorage import find_courses, get_course_by_id
from domain.data.progress.ProgressStorage import enroll_course


def overview(request: HttpRequest) -> HttpResponse:
	"""list all courses"""
	username = request.user.username #type: ignore

	return render(request, 'courses/overview.html', {
		'courses': find_courses(),
		'courses_overview': True,
		'username': username,
	})


def enroll(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	username = request.user.username #type: ignore
	course = get_course_by_id(course_id)
	if course is None: return  redirect('overview')

	if (enroll_course(username, course.database)):
		messages.success(request, 'Kurz byl zapsán')
	else:
		messages.error(request, 'Kurz nebylo možné zapsat')

	return redirect('courses:overview')
