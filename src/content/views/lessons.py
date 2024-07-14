"""views.py"""
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.CourseEditForm import CourseEditForm
from domain.data.courses.CourseDataSerializer import CourseDataSerializer
from domain.data.courses.CourseStorage import find_courses, get_course
from domain.data.lessons.LessonStorage import find_lessons
from domain.data.projects.ProjectStorage import find_projects_by_course


@staff_member_required
def lesson_edit(request: HttpRequest, course_no: str, project_no: str, lesson_no: str) -> HttpResponse:
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
def lesson_overview(request: HttpRequest, course_no: str) -> HttpResponse:
	"""list all courses"""
	course = get_course(course_no)
	if course == None: return  redirect('admin_course_overview')

	lessons = find_lessons(course=course.projects)
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/content_overview'}, {'Lessons': '#'}]

	return render(request, 'content/lessons/overview.html', {
		'course_title': course.title,
		'course_name': course.projects,
		'lessons': lessons,
		'breadcrumbs': breadcrumbs,
		'course_no': course_no,
	})
