"""views.py"""
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.CourseEditForm import CourseEditForm
from domain.data.chapters.ChapterStorage import find_chapter
from domain.data.courses.CourseDataSerializer import CourseDataSerializer
from domain.data.courses.CourseStorage import find_courses, get_course
from domain.data.projects.ProjectStorage import find_projects_by_course
from domain.data.tests.TestStorage import find_tests


@staff_member_required
def test_edit(request: HttpRequest, course_no: str) -> HttpResponse:
	pass

@staff_member_required
def test_overview(request: HttpRequest, course_no: str) -> HttpResponse:
	"""list all courses"""
	course = get_course(course_no)
	if course == None: return  redirect('admin_course_overview')
	tests = find_tests(course=course.projects)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/content_overview'}, {'Tests': '#'}]

	return render(request, 'content/tests/overview.html', {
		'course_title': course.title,
		'tests': tests,
		'breadcrumbs': breadcrumbs,
		'course_no': course_no,
	})
