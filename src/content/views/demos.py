"""views.py"""
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.DemoEditForm import DemoEditForm
from domain.data.courses.CourseStorage import CourseStorage

from domain.data.demos.DemoDataSerializer import DemoDataSerializer
from domain.data.demos.DemoStorage import DemoStorage


@staff_member_required
def demo_overview(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = CourseStorage().get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	demos = DemoStorage().find_demos(db=course.database)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'demo': '#'}]
	return render(request, 'content/demos/overview.html', {
		'course': course,
		'demos': demos,
		'breadcrumbs': breadcrumbs,
	})


@staff_member_required
def demo_edit(request: HttpRequest, course_id: str, demo_id: int) -> HttpResponse:
	course = CourseStorage().get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	demo = DemoStorage().get_demo(demo_id, course.database)
	if demo is None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = DemoEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = demo.id
			demo_data = DemoDataSerializer.from_dict(edit_form.cleaned_data)
			DemoStorage().update_demo(demo_data, course.database)
			messages.success(request, 'demo edited successfully')
			return  redirect('admin_demo_edit', course_id=course.id, demo_id=demo_data.id)
	else:
		edit_form = DemoEditForm(initial=DemoDataSerializer.to_dict(demo))

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'demo': '#'}]
	return render(request, 'content/demos/edit.html', {
		'demo': demo,
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})


@staff_member_required
def demo_new(request: HttpRequest, course_id: str) -> HttpResponse:
	course = CourseStorage().get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = DemoEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = DemoStorage().get_next_valid_id(course.database)
			demo_data = DemoDataSerializer.from_dict(edit_form.cleaned_data)
			DemoStorage().create_demo(demo_data, course.database)
			messages.success(request, 'demo successfully created')
			return  redirect('admin_demo_edit', course_id=course_id, demo_id=demo_data.id)
	else:
		edit_form = DemoEditForm()

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'New demo': '#'}]
	return render(request, 'content/demos/edit.html', {
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'course': course,
	})


@staff_member_required
def demo_delete(request: HttpRequest, course_id: str, demo_id: int) -> HttpResponse:
	course = CourseStorage().get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	demo = DemoStorage().get_demo(demo_id, course.database)
	if demo is None: return  redirect('admin_course_overview')

	DemoStorage().delete_demo(course.database, demo.id)
	messages.success(request, 'demo has been deleted')

	return redirect('admin_demo_overview', course_id=course_id)

