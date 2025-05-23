"""views.py"""
import json
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.CourseEditForm import CourseEditForm
from content.forms.CourseUploadForm import CourseUploadForm
from domain.data.courses.CourseDataSerializer import CourseDataSerializer
from domain.data.courses.CourseStorage import CourseStorage
from domain.data.database_backup.BackUpStorage import delete_all, download_json, download_json_users, upload_from_json


@staff_member_required
def course_edit(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = CourseStorage().get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = CourseEditForm(request.POST, database=course.database)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = course.id
			course_data = CourseDataSerializer.from_dict(edit_form.cleaned_data)
			CourseStorage().update_course(course_data)
			return redirect('admin_course_edit', course_id=course_data.id)
	else:
		edit_form = CourseEditForm(initial=CourseDataSerializer.to_dict(course))

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {'Edit': '#'}]
	return render(request, 'content/courses/edit.html', {
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})


@staff_member_required
def progress_download(request: HttpRequest) -> HttpResponse: #pylint: disable=W0613
	"""list all courses"""
	json_result = download_json_users()

	if json_result is None: return redirect('admin_course_overview')

	response = HttpResponse(json.dumps(json_result), content_type='application/json') #type: ignore
	response['Content-Disposition'] = 'attachment; filename=student.json'

	return response


@staff_member_required
def course_download(request: HttpRequest, course_id: str) -> HttpResponse: #pylint: disable=W0613
	"""list all courses"""
	json_result = download_json(course_id)
	if json_result is None: return redirect('admin_course_overview')
	course = CourseStorage().get_course_by_id(course_id)
	if course is None: return redirect('admin_course_overview')

	response = HttpResponse(json.dumps(json_result), content_type='application/json') #type: ignore
	response['Content-Disposition'] = f'attachment; filename={course.title}.json'
	return response


@staff_member_required
def course_new(request: HttpRequest) -> HttpResponse:
	"""list all courses"""
	if request.method == 'POST':
		edit_form = CourseEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = CourseStorage().get_next_valid_id()
			course_data = CourseDataSerializer.from_dict(edit_form.cleaned_data)
			try:
				CourseStorage().create_course(course_data)
				return redirect('admin_course_edit', course_id=course_data.id)
			except: #pylint: disable=W0702
				edit_form.add_error('database', 'This string must be unique. choose another one')
	else:
		edit_form = CourseEditForm()

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {'New': '#'}]
	return render(request, 'content/courses/edit.html', {
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})


@staff_member_required
def course_overview(request: HttpRequest) -> HttpResponse:
	"""list all courses"""
	courses = CourseStorage().find_courses()
	if request.method == 'POST':
		form = CourseUploadForm(request.POST, request.FILES)
		if form.is_valid():
			upload_result = upload_from_json(json.load(request.FILES['file'])) #type: ignore
			if upload_result is None:
				messages.success(request, 'Course successfully uploaded')
				return redirect('admin_course_overview')
			messages.warning(request, f'Problem occurred during uploading file data: {str(upload_result)}')
			return redirect('admin_course_overview')
	else:
		form = CourseUploadForm()

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '#'}]
	return render(request, 'content/courses/overview.html', {
		'courses': courses,
		'form': form,
		'breadcrumbs': breadcrumbs,
	})


@staff_member_required
def course_delete(request: HttpRequest, course_id: str) -> HttpResponse: #pylint: disable=W0613
	delete_all(course_id)
	return redirect('admin_course_overview')
