"""views.py"""
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.CourseEditForm import CourseEditForm
from content.forms.TestEditForm import TestEditForm
from domain.data.chapters.ChapterStorage import find_chapter
from domain.data.courses.CourseDataSerializer import CourseDataSerializer
from domain.data.courses.CourseStorage import find_courses, get_course, get_course_by_id
from domain.data.projects.ProjectStorage import find_projects_by_course
from domain.data.tests.TestDataSerializer import TestDataSerializer
from domain.data.tests.TestStorage import find_tests, get_test


@staff_member_required
def test_edit(request: HttpRequest, course_id: str, test_no: str) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	test, questions = get_test(course.database, test_no)
	if test == None: return  redirect('admin_course_overview')

	edit_form = TestEditForm(initial=TestDataSerializer.to_dict(test))
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/test/content_overview'}, {'Edit': '#'}]
	print(questions)
	return render(request, 'content/tests/edit.html', {
		'test': test,
		'questions': questions,
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})

@staff_member_required
def test_overview(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	tests = find_tests(db=course.database)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/content_overview'}, {'Tests': '#'}]

	return render(request, 'content/tests/overview.html', {
		'course': course,
		'tests': tests,
		'breadcrumbs': breadcrumbs,
	})
