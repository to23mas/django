"""views.py"""
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.CourseEditForm import CourseEditForm
from content.forms.LessonEditForm import LessonEditForm
from domain.data.courses.CourseDataSerializer import CourseDataSerializer
from domain.data.courses.CourseStorage import find_courses, get_course
from domain.data.lessons.LessonDataSerializer import LessonDataSerializer
from domain.data.lessons.LessonStorage import find_lessons, get_lesson
from domain.data.projects.ProjectStorage import find_projects_by_course


@staff_member_required
def lesson_edit(request: HttpRequest, course_no: str, project_no: str, lesson_no: str) -> HttpResponse:
	"""list all courses"""
	course = get_course(course_no)
	if course == None: return  redirect('admin_course_overview')
	lesson = get_lesson(lesson_no, project_no, course.projects)
	if lesson == None: return  redirect('admin_course_overview')

	edit_form = LessonEditForm(initial=LessonDataSerializer.to_dict(lesson))
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/content_overview'}, {'Edit': '#'}]
	return render(request, 'content/lessons/edit.html', {
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
