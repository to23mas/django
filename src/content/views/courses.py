"""views.py"""
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.CourseEditForm import CourseEditForm
from domain.data.courses.CourseDataSerializer import CourseDataSerializer
from domain.data.courses.CourseStorage import find_courses, get_course


@staff_member_required
def course_edit(request: HttpRequest, course_no: str) -> HttpResponse:
	"""list all courses"""
	course = get_course(course_no)
	if course == None: return  redirect('admin_course_overview')

	edit_form = CourseEditForm(initial=CourseDataSerializer.to_dict(course))
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/content_overview'}, {'Edit': '#'}]
	return render(request, 'content/courses/edit.html', {
		'course_title': course.title,
		'breadcrumbs': breadcrumbs,
		'course_no': course_no,
		'form': edit_form,
	})

@staff_member_required
def course_overview(request: HttpRequest) -> HttpResponse:
	"""list all courses"""
	courses = find_courses()
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '#'}]

	return render(request, 'content/courses/overview.html', {
		'courses': courses,
		'breadcrumbs': breadcrumbs,
	})
