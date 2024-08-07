"""views.py"""
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from content.forms.QuestionEditForm import QuestionEditForm
from content.forms.TestEditForm import TestEditForm
from domain.data.courses.CourseStorage import get_course_by_id
from domain.data.tests.QuestionDataSerializer import QuestionDataSerializer
from domain.data.tests.TestDataSerializer import TestDataSerializer
from domain.data.tests.TestStorage import create_question, create_test, delete_question, delete_test, find_tests, get_next_valid_id, get_next_valid_question_id, get_test, update_question, update_test


@staff_member_required
def test_overview(request: HttpRequest, course_id: str) -> HttpResponse:
	"""list all courses"""
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	tests = find_tests(db=course.database)

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'Tests': '#'}]
	return render(request, 'content/tests/overview.html', {
		'course': course,
		'tests': tests,
		'breadcrumbs': breadcrumbs,
	})


@staff_member_required
def test_edit(request: HttpRequest, course_id: str, test_id: int) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	test, questions = get_test(course.database, test_id)
	if test == None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = TestEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = test.id
			test_data = TestDataSerializer.from_dict(edit_form.cleaned_data)
			update_test(test_data, course.database)
			messages.success(request, 'Test edited successfully')
			return  redirect('admin_test_edit', course_id=course.id, test_id=test_data.id)

	edit_form = TestEditForm(initial=TestDataSerializer.to_dict(test))
	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'Test': '#'}]
	return render(request, 'content/tests/edit.html', {
		'test': test,
		'questions': questions,
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})


@staff_member_required
def test_new(request: HttpRequest, course_id: str) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = TestEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = get_next_valid_id(course.database)
			test_data = TestDataSerializer.from_dict(edit_form.cleaned_data)
			create_test(test_data, course.database)
			messages.success(request, 'Test succesfully created')
			return  redirect('admin_test_edit', course_id=course_id, test_id=test_data.id)
	else:
		edit_form = TestEditForm()

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}/edit'}, {'New Lesson': '#'}]
	return render(request, 'content/tests/edit.html', {
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'course': course,
	})


@staff_member_required
def test_delete(request: HttpRequest, course_id: str, test_id: int) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	test, _ = get_test(course.database, test_id)
	if test == None: return  redirect('admin_course_overview')

	delete_test(course.database, test.id)
	messages.success(request, 'Test has been deleted')
	return redirect('admin_test_overview', course_id=course_id);


@staff_member_required
def test_new_question(request: HttpRequest, course_id: str, test_id: int) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	test, _ = get_test(course.database, test_id)
	if test == None: return  redirect('admin_course_overview')

	if request.method == 'POST':
		edit_form = QuestionEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] =  get_next_valid_question_id(course.database, test_id)
			question_data = QuestionDataSerializer.from_dict(edit_form.cleaned_data)
			create_question(question_data, test_id, course.database)
			messages.success(request, 'Question successfully created')
			return  redirect('admin_test_edit_question', course_id=course.id, test_id=test.id ,question_id=question_data.id)
	else:
		edit_form = QuestionEditForm()

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {'TEST': f'/admin/content/course/{course.id}-{test.id}/test/edit'}, {'New Question': '#'}]
	return render(request, 'content/questions/edit.html', {
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
		'course': course,
	})


@staff_member_required
def test_edit_question(request: HttpRequest, course_id: str, test_id: int, question_id: int) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	test, questions = get_test(course.database, test_id)
	if test == None: return  redirect('admin_course_overview')

	question_data = [q for q in questions if q.id == question_id][0] #type: ignore

	if request.method == 'POST':
		edit_form = QuestionEditForm(request.POST)
		if edit_form.is_valid():
			edit_form.cleaned_data['_id'] = question_data.id
			question_data = QuestionDataSerializer.from_dict(edit_form.cleaned_data)
			update_question(question_data, course.database, test.id)
			messages.success(request, 'Question edited successfully')
			return  redirect('admin_test_edit_question', course_id=course.id, test_id=test.id ,question_id=question_id)

	edit_form = QuestionEditForm(initial=QuestionDataSerializer.to_dict(question_data))

	breadcrumbs = [{'Home': '/admin/'}, {'Courses': '/admin/content/'}, {f'{course.title}': f'/admin/content/course/{course.id}-{test.id}/test/edit'}, {'Editing Question': '#'}]

	return render(request, 'content/questions/edit.html', {
		'question': question_data,
		'course': course,
		'breadcrumbs': breadcrumbs,
		'form': edit_form,
	})


@staff_member_required
def test_delete_question(request: HttpRequest, course_id: str, test_id: int, question_id: int) -> HttpResponse:
	course = get_course_by_id(course_id)
	if course == None: return  redirect('admin_course_overview')
	test, _ = get_test(course.database, test_id)
	if test == None: return  redirect('admin_course_overview')

	delete_question(course.database, test.id, question_id)
	messages.success(request, 'Question has been deleted')
	return redirect('admin_test_edit', course_id=course_id, test_id=test.id);


