"""views.py"""
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.ProjectEditForm import ProjectEditForm
from domain.data.courses.CourseStorage import CourseStorage

from domain.data.projects.ProjectDataSerializer import ProjectDataSerializer
from domain.data.projects.ProjectStorage import ProjectStorage


@staff_member_required
def project_overview(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = CourseStorage().get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	projects = ProjectStorage().find_projects(course.database)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'Projects': '#'}]
	return render(request, 'content/projects/overview.html', {
		'course': course,
		'projects': projects,
		'breadcrumbs': breadcrumbs,
	})


@staff_member_required
def project_edit(request: HttpRequest, course_id: str, project_id: int) -> HttpResponse:
	"""list all courses"""
	course = CourseStorage().get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	project = ProjectStorage().get_project_by_id(project_id, course.database)
	if project is None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = ProjectEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = edit_form.cleaned_data['id']
			project_data = ProjectDataSerializer.from_dict(edit_form.cleaned_data)
			ProjectStorage().update_project(project_data, course.database)
			messages.success(request, 'Project have been updated')
			return  redirect('admin_project_edit', course_id=course_id, project_id=project_data.id)
	else:
		edit_form = ProjectEditForm(initial=ProjectDataSerializer.to_dict(project))

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'Edit Project': '#'}]
	return render(request, 'content/projects/edit.html', {
		'project': project,
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})


@staff_member_required
def project_new(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = CourseStorage().get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = ProjectEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = ProjectStorage().get_next_valid_id(course.database)
			project_data = ProjectDataSerializer.from_dict(edit_form.cleaned_data)
			try:
				ProjectStorage().create_project(project_data, course.database)
				return  redirect('admin_project_edit', course_id=course_id, project_id=project_data.id)
			except: #pylint: disable=W0702
				edit_form.add_error('database', 'This value must be unique')
	else:
		edit_form = ProjectEditForm()

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'New Project': '#'}]
	return render(request, 'content/projects/edit.html', {
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'course': course,
	})


@staff_member_required
def project_delete(request: HttpRequest, course_id: str, project_no: str) -> HttpResponse: #pylint: disable=W0613
	course = CourseStorage().get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')

	project = ProjectStorage().get_project(course.database, {'_id': int(project_no)})
	if project is None: return  redirect('admin_course_overview')

	ProjectStorage().delete_project(course.database, project.id)
	return redirect('admin_project_overview', course_id=course_id)
