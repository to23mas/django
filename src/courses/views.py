from django.contrib import messages
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from domain.data.courses.CourseStorage import CourseStorage
from domain.data.progress.ProgressStorage import ProgressStorage
from domain.data.progress.enum.ProgressState import ProgressState

def calculate_course_progress(progress: dict | None) -> int:
	if progress is None:
		return 0
	
	total_items = 0
	completed_items = 0
	
	for project_id, project_state in progress['projects'].items():
		for _, chapter_state in progress['chapters'][project_id].items():
			if chapter_state == ProgressState.DONE.value:
				completed_items += 1
			total_items += 1

	if total_items == 0:
		return 0
		
	return int((completed_items / total_items) * 100)

@login_required(login_url='/users/login/')
def overview(request: HttpRequest) -> HttpResponse:
	"""list all courses"""
	username = request.user.username #type: ignore
	courses = CourseStorage().find_courses()
	
	course_progress = {}
	for course in courses:
		progress = ProgressStorage().get_user_progress_by_course(username, course.database)
		course_progress[course.database] = calculate_course_progress(progress)

	return render(request, 'courses/overview.html', {
		'courses': courses,
		'courses_overview': True,
		'username': username,
		'course_progress': course_progress,
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
