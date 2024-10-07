"""views.py"""
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.BlocklyEditForm import BlocklyEditForm
from domain.data.blockly.BlocklyDataSerializer import BlocklyDataSerializer
from domain.data.blockly.BlocklyStorage import create_blockly, delete_blockly, find_blockly, get_blockly, get_next_valid_id, update_blockly
from domain.data.courses.CourseStorage import get_course_by_id


@staff_member_required
def blockly_overview(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	blocklys = find_blockly(db=course.database)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'Blockly': '#'}]
	return render(request, 'content/blockly/overview.html', {
		'course': course,
		'blocklys': blocklys,
		'breadcrumbs': breadcrumbs,
	})


@staff_member_required
def blockly_edit(request: HttpRequest, course_id: str, blockly_id: int) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	blockly = get_blockly(course.database, blockly_id)
	if blockly is None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = BlocklyEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = blockly.id
			blockly_data = BlocklyDataSerializer.from_dict(edit_form.cleaned_data)
			update_blockly(blockly_data, course.database)
			messages.success(request, 'Blockly edited successfully')
			return  redirect('admin_blockly_edit', course_id=course.id, blockly_id=blockly_data.id)
	else:
		edit_form = BlocklyEditForm(initial=BlocklyDataSerializer.to_dict(blockly))

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'Blockly': '#'}]
	return render(request, 'content/blockly/edit.html', {
		'blockly': blockly,
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})


@staff_member_required
def blockly_new(request: HttpRequest, course_id: str) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = BlocklyEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = get_next_valid_id(course.database)
			blockly_data = BlocklyDataSerializer.from_dict(edit_form.cleaned_data)
			create_blockly(blockly_data, course.database)
			messages.success(request, 'Blockly successfully created')
			return  redirect('admin_blockly_edit', course_id=course_id, blockly_id=blockly_data.id)
	else:
		edit_form = BlocklyEditForm()

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'New Blockly': '#'}]
	return render(request, 'content/blockly/edit.html', {
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'course': course,
	})


@staff_member_required
def blockly_delete(request: HttpRequest, course_id: str, blockly_id: int) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	blockly = get_blockly(course.database, blockly_id)
	if blockly is None: return  redirect('admin_course_overview')

	delete_blockly(course.database, blockly.id)
	messages.success(request, 'Blockly has been deleted')
	return redirect('admin_blockly_overview', course_id=course_id)
