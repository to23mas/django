"""views.py"""
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.CourseEditForm import CourseEditForm
from domain.data.chapters.ChapterStorage import find_chapter
from domain.data.courses.CourseDataSerializer import CourseDataSerializer
from domain.data.courses.CourseStorage import find_courses, get_course, get_course_by_id
from domain.data.projects.ProjectStorage import find_projects_by_course


@staff_member_required
def chapter_edit(request: HttpRequest, course_no: str) -> HttpResponse:
	pass

@staff_member_required
def chapter_overview(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	chapters = find_chapter(db=course.database)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/content_overview'}, {'Chapters': '#'}]

	return render(request, 'content/chapters/overview.html', {
		'course': course,
		'chapters': chapters,
		'breadcrumbs': breadcrumbs,
	})
