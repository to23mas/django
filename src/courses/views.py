from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from domain.data.courses.CourseStorage import find_courses, get_course_by_id
from domain.data.progress.ProgressStorage import enroll_course


@login_required
def overview(request: HttpRequest) -> HttpResponse:
	"""list all courses"""
	username = request.user.username #type: ignore
	messages.success(request, 'Kurz byl zapsán')
	messages.success(request, 'Kurz byl zapsán')
	messages.success(request, 'Kurz byl zapsán')

	return render(request, 'courses/overview.html', {
		'courses': find_courses(),
		'courses_overview': True,
		'username': username,
	})


@login_required
def enroll(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	username = request.user.username #type: ignore
	course = get_course_by_id(course_id)
	messages.success(request, 'Kurz byl zapsán')
	if course == None: return  redirect('overview')

	if (enroll_course(username, course.database)):
		messages.success(request, 'Kurz byl zapsán')
	else:
		messages.error(request, 'Kurz nebylo možné zapsat')

	return redirect('courses:overview')
