"""views.py"""
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.CourseEditForm import CourseEditForm
from content.forms.ProjectEditForm import ProjectEditForm
from domain.data.courses.CourseDataSerializer import CourseDataSerializer
from domain.data.courses.CourseStorage import find_courses, get_course
from domain.data.projects.ProjectDataSerializer import ProjectDataSerializer
from domain.data.projects.ProjectStorage import find_projects_by_course, get_project


@staff_member_required
def project_edit(request: HttpRequest, course_no: str, project_no: str) -> HttpResponse:
	"""list all courses"""
	course = get_course(course_no)
	if course == None: return  redirect('admin_course_overview')
	project, lessons_graph = get_project(int(project_no), course.projects)
	if project == None: return  redirect('admin_course_overview')

	__import__('pprint').pprint(project)
	edit_form = ProjectEditForm(initial=ProjectDataSerializer.to_dict(project))
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/content_overview'}, {'Edit': '#'}]
	return render(request, 'content/projects/edit.html', {
		'course_title': course.title,
		'breadcrumbs': breadcrumbs,
		'course_no': course_no,
		'form': edit_form,
	})

@staff_member_required
def project_overview(request: HttpRequest, course_no: str) -> HttpResponse:
	"""list all courses"""
	course = get_course(course_no)
	if course == None: return  redirect('admin_course_overview')
	projects = find_projects_by_course(course.projects)
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/content_overview'}, {'Projects': '#'}]

	return render(request, 'content/projects/overview.html', {
		'course_title': course.title,
		'projects': projects,
		'breadcrumbs': breadcrumbs,
		'course_no': course_no,
	})
