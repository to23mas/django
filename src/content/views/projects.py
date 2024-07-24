"""views.py"""
from bson.objectid import ObjectId
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.ProjectEditForm import ProjectEditForm
from domain.data.courses.CourseStorage import get_course_by_id
from domain.data.projects.ProjectDataSerializer import ProjectDataSerializer
from domain.data.projects.ProjectStorage import create_project, delete_project, exists_project, find_projects, get_project


@staff_member_required
def project_overview(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	projects = find_projects(course.database)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'Projects': '#'}]
	return render(request, 'content/projects/overview.html', {
		'course': course,
		'projects': projects,
		'breadcrumbs': breadcrumbs,
	})


@staff_member_required
def project_edit(request: HttpRequest, course_id: str, project_id: int) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	project, lessons_graph = get_project(project_id, course.database)
	if project == None: return  redirect('admin_course_overview')

	edit_form = ProjectEditForm(initial=ProjectDataSerializer.to_dict(project))
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'Edit Project': '#'}]
	return render(request, 'content/projects/edit.html', {
		'project': project,
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'lessons_graph': lessons_graph,
	})


@staff_member_required
def project_new(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = ProjectEditForm(request.POST)
		if edit_form.is_valid():
			if exists_project(course.database, edit_form.cleaned_data['no']):
				edit_form.add_error('no', 'This number already exists in the database. Must be unique.')
			else:
				edit_form.cleaned_data['_id'] = ObjectId()
				project_data = ProjectDataSerializer.from_dict(edit_form.cleaned_data)
				create_project(project_data, course.database)
				return  redirect('admin_project_edit', course_id=course_id, project_id=project_data.id)

	else:
		edit_form = ProjectEditForm()

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'New Project': '#'}]
	return render(request, 'content/projects/edit.html', {
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'course': course,
	})


@staff_member_required
def project_delete(request: HttpRequest, course_id: str, project_no: str) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	project, _ = get_project(int(project_no), course.database)
	if project == None: return  redirect('admin_course_overview')

	delete_project(course.database, project.id)
	return redirect('admin_project_overview', course_id=course_id);
