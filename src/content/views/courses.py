"""views.py"""
import json
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.CourseEditForm import CourseEditForm
from content.forms.CourseUploadForm import CourseUploadForm
from domain.data.chapters.ChapterDataSerializer import ChapterDataSerializer
from domain.data.chapters.ChapterStorage import find_chapters
from domain.data.courses.CourseDataSerializer import CourseDataSerializer
from domain.data.courses.CourseStorage import create_course, delete_course, find_courses, get_course_by_id, get_next_valid_id, update_course
from domain.data.lessons.LessonDataSerializer import LessonDataSerializer
from domain.data.lessons.LessonStorage import find_lessons
from domain.data.projects.ProjectDataSerializer import ProjectDataSerializer
from domain.data.projects.ProjectStorage import find_projects
from domain.data.tests.QuestionDataSerializer import QuestionDataSerializer
from domain.data.tests.TestDataSerializer import TestDataSerializer
from domain.data.tests.TestStorage import find_tests, get_test


@staff_member_required
def course_edit(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		print(request.POST)
		edit_form = CourseEditForm(request.POST, database=course.database)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = course.id
			course_data = CourseDataSerializer.from_dict(edit_form.cleaned_data)
			update_course(course_data)
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
def course_download(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	#COURSE
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	json_result = {'course': CourseDataSerializer.to_dict(course)}

	#PROJECTS LESSONS CHAPTERS
	projects = find_projects(course.database)
	json_result['projects'] = [] #type: ignore
	for project in projects:
		project_dict = ProjectDataSerializer.to_dict(project)

		lessons = find_lessons(course.database, project.database)
		if lessons == None:
			json_result['projects'].append(project_dict)
			continue
		project_dict['lessons'] = [LessonDataSerializer.to_dict(lesson) for lesson in lessons] #type: ignore

		chapters = find_chapters(course.database, project.database)
		if chapters == None:
			continue
		project_dict['chapters'] = [ChapterDataSerializer.to_dict(chapter) for chapter in chapters] #type: ignore

		json_result['projects'].append(project_dict)

	tests = find_tests(course.database)
	json_result['tests'] = [] #type: ignore
	if tests != None:
		for t in tests:
			_, questions = get_test(course.database, t.id)
			test_dict = TestDataSerializer.to_dict(t)
			if questions != None:
				test_dict['questions'] = [QuestionDataSerializer.to_dict(question) for question in questions] #type: ignore
			json_result['tests'].append(test_dict)

	__import__('pprint').pprint(json_result)
	response = HttpResponse(json.dumps(json_result), content_type='application/json') #type: ignore
	response['Content-Disposition'] = f'attachment; filename={course.title}.json'
	return response


@staff_member_required
def course_new(request: HttpRequest) -> HttpResponse:
	"""list all courses"""

	# UPLOADING migration files
	if request.method == 'POST':
		edit_form = CourseEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = get_next_valid_id()
			course_data = CourseDataSerializer.from_dict(edit_form.cleaned_data)
			try:
				create_course(course_data)
				return redirect('admin_course_edit', course_id=course_data.id)
			except:
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
	courses = find_courses()
	if request.method == 'POST':
		form = CourseUploadForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['file']
			file_data = json.load(file) #type: ignore
			print(CourseDataSerializer.from_dict(file_data))
			try:
				create_course(CourseDataSerializer.from_dict(file_data))
				return redirect('admin_course_overview');
			except Exception as e:
				messages.warning(request, f'Problem occurred during uploading file data: {str(e)}')
	else:
		form = CourseUploadForm()


	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '#'}]

	return render(request, 'content/courses/overview.html', {
		'courses': courses,
		'form': form,
		'breadcrumbs': breadcrumbs,
	})


@staff_member_required
def course_delete(request: HttpRequest, course_id: str) -> HttpResponse:
	delete_course(course_id)
	return redirect('admin_course_overview');
