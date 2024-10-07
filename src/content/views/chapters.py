"""views.py"""
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.ChapterEditForm import ChapterEditForm
from content.forms.ChapterFilterForm import ChapterFilterForm
from domain.data.chapters.ChapterDataSerializer import ChapterDataSerializer
from domain.data.chapters.ChapterStorage import create_chapter, delete_chapter, find_chapters, get_chapter, get_next_valid_id, update_chapter
from domain.data.courses.CourseStorage import get_course_by_id
from domain.data.projects.ProjectStorage import get_project_by_id


@staff_member_required
def chapter_overview(request: HttpRequest, course_id: str, project_id: int) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	project = get_project_by_id(project_id, course.database)
	if project is None: return  redirect('admin_course_overview')

	filter_ = ChapterFilterForm(db=course.database, project_db=project.database)
	if request.method == 'POST':
		filter_ = ChapterFilterForm(request.POST, db=course.database, project_db=project.database)
		if filter_.is_valid():
			chapters = find_chapters(course.database, project.database, filter_.cleaned_data)
		else:
			chapters = find_chapters(course.database, project.database)
	else:
		chapters = find_chapters(course.database, project.database)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'Chapters': '#'}]
	return render(request, 'content/chapters/overview.html', {
		'course': course,
		'chapters': chapters,
		'project': project,
		'breadcrumbs': breadcrumbs,
		'filter': filter_,
	})


@staff_member_required
def chapter_edit(request: HttpRequest, course_id: str, project_id: int, lesson_id: int, chapter_id: int) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	project = get_project_by_id(project_id, course.database)
	if project is None: return  redirect('admin_course_overview')
	chapter = get_chapter(chapter_id, lesson_id, course.database, project.database)
	if chapter is None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = ChapterEditForm(request.POST, db=course.database, project_db=project.database)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = edit_form.cleaned_data['id']
			chapter_data = ChapterDataSerializer.from_dict(edit_form.cleaned_data, chapter)
			update_chapter(chapter_data, course.database, project.database, chapter.lesson_id)
			messages.success(request, 'Chapter has been updated')
			return  redirect('admin_chapter_edit', course_id=course_id, project_id=project.id, lesson_id=chapter_data.lesson_id, chapter_id=chapter_data.id)
	else:
		edit_form = ChapterEditForm(initial=ChapterDataSerializer.to_dict(chapter), db=course.database, project_db=project.database)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'Edit Chapters': '#'}]
	return render(request, 'content/chapters/edit.html', {
		'chapter': chapter,
		'course': course,
		'project': project,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})


@staff_member_required
def chapter_new(request: HttpRequest, course_id: str, project_id: int) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	project = get_project_by_id(project_id, course.database)
	if project is None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = ChapterEditForm(request.POST, db=course.database, project_db=project.database)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = get_next_valid_id(course.database, project.database)
			chapter_data = ChapterDataSerializer.from_dict(edit_form.cleaned_data)
			create_chapter(chapter_data, course.database, project.database)
			messages.success(request, 'Chapter has been created')
			return  redirect('admin_chapter_edit', course_id=course_id, project_id=project.id, lesson_id=chapter_data.lesson_id, chapter_id=chapter_data.id)
	else:
		edit_form = ChapterEditForm(db=course.database, project_db=project.database)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'New Chapter': '#'}]
	return render(request, 'content/chapters/edit.html', {
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'course': course,
		'project': project,
	})


@staff_member_required
def chapter_delete(request: HttpRequest, course_id: str, project_id: int, lesson_id: int, chapter_id: int) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	project = get_project_by_id(project_id, course.database)
	if project is None: return  redirect('admin_course_overview')
	chapter = get_chapter(chapter_id, lesson_id, course.database, project.database)
	if chapter is None: return  redirect('admin_course_overview')

	delete_chapter(course.database, project.database, chapter.id, chapter.lesson_id)
	messages.success(request, 'Chapter has been deleted')
	return redirect('admin_chapter_overview', course_id=course_id, project_id=project.id)
