"""views.py"""
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.CourseEditForm import CourseEditForm
from content.forms.ProjectEditForm import ProjectEditForm
from domain.data.courses.CourseDataSerializer import CourseDataSerializer
from domain.data.courses.CourseStorage import find_courses, get_course, get_course_by_id
from domain.data.projects.ProjectDataSerializer import ProjectDataSerializer
from domain.data.projects.ProjectStorage import find_projects_by_course, get_project


@staff_member_required
def project_edit(request: HttpRequest, course_id: str, project_no: str) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	project, lessons_graph = get_project(int(project_no), course.database)
	if project == None: return  redirect('admin_course_overview')

	edit_form = ProjectEditForm(initial=ProjectDataSerializer.to_dict(project))
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/content_overview'}, {'Edit': '#'}]
	return render(request, 'content/projects/edit.html', {
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'lessons_graph': lessons_graph,
	})

@staff_member_required
def project_overview(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	projects = find_projects_by_course(course.database)
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/content_overview'}, {'Projects': '#'}]

	return render(request, 'content/projects/overview.html', {
		'course': course,
		'projects': projects,
		'breadcrumbs': breadcrumbs,
	})
