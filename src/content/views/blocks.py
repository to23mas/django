"""views.py"""
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.BlockEditForm import BlockEditForm
from domain.data.chapters.ChapterStorage import create_block, delete_block, get_chapter, get_next_valid_block_id, update_block
from domain.data.courses.CourseStorage import get_course_by_id
from domain.data.projects.ProjectStorage import get_project_by_id



@staff_member_required
def block_edit(request: HttpRequest, course_id: str, project_id: int, lesson_id: int, chapter_id: int, block_id: int) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	project = get_project_by_id(project_id, course.database)
	if project is None: return  redirect('admin_course_overview')
	chapter = get_chapter(chapter_id, lesson_id, course.database, project.database)
	if chapter is None: return  redirect('admin_course_overview')

	block = [ b for b in chapter.blocks if b['id'] == block_id ][0] #type: ignore

	if request.method == 'POST':
		edit_form = BlockEditForm(request.POST)
		if edit_form.is_valid():
			update_block(chapter, course.database, project.database, block_id, edit_form.cleaned_data)
			messages.success(request, 'Block has been updated')
			return  redirect('admin_block_edit', course_id=course_id, project_id=project.id, lesson_id=chapter.lesson_id, chapter_id=chapter.id, block_id=block_id)
	else:
		edit_form = BlockEditForm(initial=block)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'Edit Chapters': '#'}]
	return render(request, 'content/blocks/edit.html', {
		'chapter': chapter,
		'block': block,
		'course': course,
		'project': project,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})


@staff_member_required
def block_new(request: HttpRequest, course_id: str, project_id: int, lesson_id: int, chapter_id: int) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	project = get_project_by_id(project_id, course.database)
	if project is None: return  redirect('admin_course_overview')
	chapter = get_chapter(chapter_id, lesson_id, course.database, project.database)
	if chapter is None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = BlockEditForm(request.POST)
		if edit_form.is_valid():
			block_id = edit_form.cleaned_data['id'] = get_next_valid_block_id(course.database, chapter.id, chapter.lesson_id, project.database)
			create_block(chapter, course.database, project.database, edit_form.cleaned_data)
			messages.success(request, 'Block has been created')
			return  redirect('admin_block_edit', course_id=course_id, project_id=project.id, lesson_id=chapter.lesson_id, chapter_id=chapter.id, block_id=block_id)
	else:
		edit_form = BlockEditForm()

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'New Chapter': '#'}]
	return render(request, 'content/blocks/edit.html', {
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'course': course,
		'project': project,
		'chapter': chapter,
	})


@staff_member_required
def block_delete(request: HttpRequest, course_id: str, project_id: int, lesson_id: int, chapter_id: int, block_id: int) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course is None: return  redirect('admin_course_overview')
	project = get_project_by_id(project_id, course.database)
	if project is None: return  redirect('admin_course_overview')
	chapter = get_chapter(chapter_id, lesson_id, course.database, project.database)
	if chapter is None: return  redirect('admin_course_overview')

	delete_block(course.database, project.database, chapter.id, chapter.lesson_id, block_id)
	messages.success(request, 'Chapter has been deleted')
	return redirect('admin_chapter_edit', course_id=course_id, project_id=project.id, lesson_id=chapter.lesson_id, chapter_id=chapter.id)
