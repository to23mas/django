from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse

from content.forms.CLIEditForm import CLIEditForm
from domain.data.clis.CliDataSerializer import CliDataSerializer
from domain.data.clis.CliStorage import CliStorage
from domain.data.courses.CourseStorage import CourseStorage


@staff_member_required
def cli_overview(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all CLI tasks"""
	course = CourseStorage().get_course_by_id(course_id)
	if course is None:
		return redirect('admin_course_overview')

	cli_tasks = CliStorage().find_cli(db=course.database)

	breadcrumbs = [
		{'Home': '/admin/'},
		{'Courses': '/admin/content/'},
		{f'{course.title}': f'/admin/content/course/{course.id}/edit'},
		{'CLI Tasks': '#'}
	]

	return render(request, 'content/cli/overview.html', {
		'course': course,
		'clis': cli_tasks,
		'breadcrumbs': breadcrumbs,
	})

@staff_member_required
def cli_edit(request: HttpRequest, course_id: str, cli_id: int) -> HttpResponse:
	course = CourseStorage().get_course_by_id(course_id)
	if course is None:
		return redirect('admin_course_overview')

	cli_task = CliStorage().get_cli(course.database, cli_id)
	if cli_task is None:
		return redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = CLIEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = cli_task.id
			cli_data = CliDataSerializer.from_dict(edit_form.cleaned_data)
			CliStorage().update_cli(cli_data, course.database)
			messages.success(request, 'CLI task edited successfully')
			return redirect('admin_cli_edit', course_id=course.id, cli_id=cli_data.id)
	else:
		edit_form = CLIEditForm(initial=CliDataSerializer.to_dict(cli_task))

	breadcrumbs = [
		{'Home': '/admin/'},
		{'Courses': '/admin/content/'},
		{f'{course.title}': f'/admin/content/course/{course.id}/edit'},
		{'CLI Tasks': '#'}
	]

	return render(request, 'content/cli/edit.html', {
		'cli': cli_task,
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})

@staff_member_required
def cli_new(request: HttpRequest, course_id: str) -> HttpResponse:
	course = CourseStorage().get_course_by_id(course_id)
	if course is None:
		return redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = CLIEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = CliStorage().get_next_valid_id(course.database)
			cli_data = CliDataSerializer.from_dict(edit_form.cleaned_data)
			CliStorage().create_cli(cli_data, course.database)
			messages.success(request, 'CLI task successfully created')
			return redirect('admin_cli_edit', course_id=course_id, cli_id=cli_data.id)
	else:
		edit_form = CLIEditForm()

	breadcrumbs = [
		{'Home': '/admin/'},
		{'Courses': '/admin/content/'},
		{f'{course.title}': f'/admin/content/course/{course.id}/edit'},
		{'New CLI Task': '#'}
	]

	return render(request, 'content/cli/edit.html', {
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'course': course,
	})

@staff_member_required
def cli_delete(request: HttpRequest, course_id: str, cli_id: int) -> HttpResponse:
	course = CourseStorage().get_course_by_id(course_id)
	if course is None:
		return redirect('admin_course_overview')

	cli_task = CliStorage().get_cli(course.database, cli_id)
	if cli_task is None:
		return redirect('admin_course_overview')

	CliStorage().delete_cli(course.database, cli_task.id)
	messages.success(request, 'CLI task has been deleted')
	return redirect('admin_cli_overview', course_id=course_id)
