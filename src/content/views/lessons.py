"""views.py"""
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.CourseEditForm import CourseEditForm
from content.forms.LessonEditForm import LessonEditForm
from domain.data.courses.CourseDataSerializer import CourseDataSerializer
from domain.data.courses.CourseStorage import find_courses, get_course, get_course_by_id
from domain.data.lessons.LessonDataSerializer import LessonDataSerializer
from domain.data.lessons.LessonStorage import find_lessons, get_lesson
from domain.data.projects.ProjectStorage import find_projects_by_course


@staff_member_required
def lesson_edit(request: HttpRequest, course_id: str, project_no: str, lesson_no: str) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	lesson = get_lesson(lesson_no, project_no, course.database)
	if lesson == None: return  redirect('admin_course_overview')

	edit_form = LessonEditForm(initial=LessonDataSerializer.to_dict(lesson))
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/content_overview'}, {'Edit': '#'}]
	return render(request, 'content/lessons/edit.html', {
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})

@staff_member_required
def lesson_overview(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')

	lessons = find_lessons(db=course.database)
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/content_overview'}, {'Lessons': '#'}]

	return render(request, 'content/lessons/overview.html', {
		'course': course,
		'lessons': lessons,
		'breadcrumbs': breadcrumbs,
	})
