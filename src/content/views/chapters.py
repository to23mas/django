"""views.py"""
from bson.objectid import ObjectId
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.ChapterEditForm import ChapterEditForm
from content.forms.ChapterFilterForm import ChapterFilterForm
from domain.data.chapters.ChapterDataSerializer import ChapterDataSerializer
from domain.data.chapters.ChapterStorage import create_chapter, exists_chapter, find_chapter, get_chapter
from domain.data.courses.CourseStorage import get_course_by_id
from domain.data.lessons.LessonStorage import get_lesson_unique_no
from domain.data.projects.ProjectStorage import get_project


@staff_member_required
def chapter_overview(request: HttpRequest, course_id: str, project_id: int) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	project, _ = get_project(project_id, course.database)
	if project == None: return  redirect('admin_course_overview')

	filter = ChapterFilterForm(db=course.database, project_db=project.database)
	if request.method == 'POST':
		filter = ChapterFilterForm(request.POST, db=course.database, project_db=project.database)
		if filter.is_valid():
			print(filter.cleaned_data)
			chapters = find_chapter(course.database, project.database, filter.cleaned_data)
		else:
			chapters = find_chapter(course.database, project.database)
	else:
		chapters = find_chapter(course.database, project.database)


	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'Chapters': '#'}]
	return render(request, 'content/chapters/overview.html', {
		'course': course,
		'chapters': chapters,
		'project': project,
		'breadcrumbs': breadcrumbs,
		'filter': filter,
	})


@staff_member_required
def chapter_edit(request: HttpRequest, course_id: str, project_id: int, lesson_id: int, chapter_id: int) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	chapter = get_chapter(project_no, lesson_no, chapter_no, course.database)
	if chapter == None: return  redirect('admin_course_overview')

	edit_form = ChapterEditForm(initial=ChapterDataSerializer.to_dict(chapter))
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'Edit Chapters': '#'}]
	return render(request, 'content/chapters/edit.html', {
		'chapter': chapter,
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})


@staff_member_required
def chapter_new(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = ChapterEditForm(request.POST, db=course.database)
		if edit_form.is_valid():
			lesson = get_lesson_unique_no(edit_form.cleaned_data['lesson'], course.database)
			if exists_chapter(course.database, edit_form.cleaned_data['no'], str(lesson.project), edit_form.cleaned_data['lesson']):
				edit_form.add_error('no', 'This number already exists in the database. Must be unique.')
			else:
				edit_form.cleaned_data['_id'] = ObjectId()
				edit_form.cleaned_data[''] = ObjectId()
				edit_form.cleaned_data['project'] = lesson.project #type: ignore
				chapter_data = ChapterDataSerializer.from_dict(edit_form.cleaned_data)
				create_chapter(chapter_data, course.database)
				messages.success(request, 'Chapter has been created')
				return  redirect('admin_chapter_edit', course_id=course_id, project_no=lesson.project, lesson_no=lesson.no, chapter_no=chapter_data.no)#type: ignore
	else:
		edit_form = ChapterEditForm(db=course.database)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'New Chapter': '#'}]
	return render(request, 'content/chapters/edit.html', {
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'course': course,
	})


@staff_member_required
def chapter_delete(request: HttpRequest, course_id: str, project_no: str, lesson_no: str, chapter_no: str) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	lesson = get_lesson(lesson_no, project_no, course.database)
	if lesson == None: return  redirect('admin_course_overview')

	delete_lesson(course.database, lesson.id)
	return redirect('admin_lesson_overview', course_id=course_id);
