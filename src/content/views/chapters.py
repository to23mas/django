"""views.py"""
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.ChapterEditForm import ChapterEditForm
from domain.data.chapters.ChapterDataSerializer import ChapterDataSerializer
from domain.data.chapters.ChapterStorage import find_chapter, get_chapter
from domain.data.courses.CourseStorage import find_courses, get_course, get_course_by_id


@staff_member_required
def chapter_edit(request: HttpRequest, course_id: str, project_no: str, lesson_no: str, chapter_no: str) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	chapter = get_chapter(project_no, lesson_no, chapter_no, course.database)
	if chapter == None: return  redirect('admin_course_overview')

	edit_form = ChapterEditForm(initial=ChapterDataSerializer.to_dict(chapter))
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/content_overview'}, {'Edit': '#'}]
	return render(request, 'content/chapters/edit.html', {
		'chapter': chapter,
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})

@staff_member_required
def chapter_overview(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	chapters = find_chapter(db=course.database)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/content_overview'}, {'Chapters': '#'}]

	return render(request, 'content/chapters/overview.html', {
		'course': course,
		'chapters': chapters,
		'breadcrumbs': breadcrumbs,
	})
