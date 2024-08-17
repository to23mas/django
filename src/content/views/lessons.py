"""views.py"""
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from content.forms.LessonEditForm import LessonEditForm
from domain.data.chapters.ChapterStorage import find_chapters
from domain.data.courses.CourseStorage import get_course_by_id
from domain.data.lessons.LessonDataSerializer import LessonDataSerializer
from domain.data.lessons.LessonStorage import create_lesson, delete_lesson, find_lessons, get_lesson, get_next_valid_id, update_lesson
from domain.data.projects.ProjectStorage import get_project_by_id


@staff_member_required
def lesson_overview(request: HttpRequest, course_id: str, project_id: int) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	project = get_project_by_id(project_id, course.database)
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
def lesson_edit(request: HttpRequest, course_id: str, project_id: int, lesson_id: int) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	project = get_project_by_id(project_id, course.database)
	if project == None: return  redirect('admin_course_overview')
	lesson = get_lesson(lesson_id, course.database, project.database)
	if lesson == None: return redirect('admin_course_overview')

	chapters = find_chapters(course.database, project.database, {'lesson_id': lesson.id})

	if request.method == 'POST':
		edit_form = LessonEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = edit_form.cleaned_data['id']
			lesson_data = LessonDataSerializer.from_dict(edit_form.cleaned_data)
			update_lesson(lesson_data, course.database, project.database)
			messages.success(request, 'Lesson has been updated')
			return  redirect('admin_lesson_edit', course_id=course_id, project_id=project.id, lesson_id=lesson_data.id)
	else:
		edit_form = LessonEditForm(initial=LessonDataSerializer.to_dict(lesson))

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {'Edit Lesson': '#'}]
	return render(request, 'content/lessons/edit.html', {
		'chapters': chapters,
		'lesson': lesson,
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'project': project,
	})


@staff_member_required
def lesson_new(request: HttpRequest, course_id: str, project_id: int) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	project = get_project_by_id(project_id, course.database)
	if project == None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = LessonEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = get_next_valid_id(course.database, project.database)
			lesson_data = LessonDataSerializer.from_dict(edit_form.cleaned_data)
			create_lesson(lesson_data, course.database, project.database)
			messages.success(request, 'Lesson has been created')
			return  redirect('admin_lesson_edit', course_id=course_id, project_id=project.id, lesson_id=lesson_data.id)
	else:
		edit_form = LessonEditForm()

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'New Lesson': '#'}]
	return render(request, 'content/lessons/edit.html', {
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'course': course,
		'project': project,
	})


@staff_member_required
def lesson_delete(request: HttpRequest, course_id: str, project_id: int, lesson_id: int) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	project = get_project_by_id(project_id, course.database)
	if project == None: return  redirect('admin_course_overview')
	lesson = get_lesson(lesson_id, course.database, project.database)
	if lesson == None: return redirect('admin_course_overview')

	delete_lesson(course.database, project.database, lesson.id)
	messages.success(request, 'Lesson has been deleted')
	return redirect('admin_lesson_overview', course_id=course_id, project_id=project.id);
