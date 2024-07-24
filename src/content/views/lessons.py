"""views.py"""
from bson.objectid import ObjectId
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from content.forms.LessonEditForm import LessonEditForm
from domain.data.courses.CourseStorage import get_course_by_id
from domain.data.lessons.LessonDataSerializer import LessonDataSerializer
from domain.data.lessons.LessonStorage import create_lesson, delete_lesson, exists_lesson, find_lessons, get_lesson
from domain.data.projects.ProjectStorage import get_project


@staff_member_required
def lesson_overview(request: HttpRequest, course_id: str, project_id: int) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	project, _ = get_project(project_id, course.database)
	if project == None: return  redirect('admin_course_overview')

	lessons = find_lessons(course.database, project.database)
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'Lessons': '#'}]
	return render(request, 'content/lessons/overview.html', {
		'course': course,
		'lessons': lessons,
		'project': project,
		'breadcrumbs': breadcrumbs,
	})


@staff_member_required
def lesson_edit(request: HttpRequest, course_id: str, project_id: int, lesson_id: id) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return redirect('admin_course_overview')
	lesson = get_lesson(lesson_no, project_no, course.database)
	if lesson == None: return redirect('admin_course_overview')

	edit_form = LessonEditForm(db=course.database, initial=LessonDataSerializer.to_dict(lesson))
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {'Edit Lesson': '#'}]
	return render(request, 'content/lessons/edit.html', {
		'lesson': lesson,
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})


@staff_member_required
def lesson_new(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = LessonEditForm(request.POST, db=course.database)
		if edit_form.is_valid():
			if exists_lesson(course.database, edit_form.cleaned_data['no']):
				edit_form.add_error('no', 'This number already exists in the database. Must be unique.')
			else:
				edit_form.cleaned_data['_id'] = ObjectId()
				edit_form.cleaned_data['project'] = int(edit_form.cleaned_data['project'])
				lesson_data = LessonDataSerializer.from_dict(edit_form.cleaned_data)
				create_lesson(lesson_data, course.database)
				messages.success(request, 'Lesson has been created')
				return  redirect('admin_lesson_edit', course_id=course_id, project_no=lesson_data.project, lesson_no=lesson_data.no)

	else:
		edit_form = LessonEditForm(db=course.database)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'New Lesson': '#'}]
	return render(request, 'content/lessons/edit.html', {
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'course': course,
	})


@staff_member_required
def lesson_delete(request: HttpRequest, course_id: str, project_id: int, lesson_id: id) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	lesson = get_lesson(lesson_no, project_no, course.database)
	if lesson == None: return  redirect('admin_course_overview')

	delete_lesson(course.database, lesson.id)
	return redirect('admin_lesson_overview', course_id=course_id);
