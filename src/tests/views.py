from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from domain.data.chapters.ChapterStorage import get_chapter_by_id
from domain.data.progress.ProgressStorage import find_available_tests, is_chapter_open
from domain.data.projects.ProjectStorage import get_project_by_id
from domain.data.tests.TestResultSerializer import TestResultSerializer
from domain.data.tests.TestStorage import find_tests_for_overview, get_test


from domain.data.tests.enum.TestState import TestState
from domain.data.tests_progress.TestProgressStorage import get_test_progress, unlock_test
from tests.forms import DynamicTestForm
from tests.utils import validate_test_get_result


@login_required
def overview(request: HttpRequest, course: str) -> HttpResponse:
	"""list of all available tests"""

	username = request.user.username #type: ignore
	user_available = find_available_tests(course, username)

	if user_available == None or len(user_available) == 0:
		messages.success(request, 'V tuto chvíli nemáš žádné dostupné testy')
		return render(request, 'tests/overview.html', {
			'course': course,
		})

	available_tests = find_tests_for_overview(course, user_available)

	return render(request, 'tests/overview.html', {
		'tests': available_tests,
		'course': course,
		'username': username,
	})


def unlock(request: HttpRequest, course: str, test_id: int, project_id: int) -> HttpResponse:
	"""list of all available tests"""
	username = request.user.username #type: ignore

	test_progress = get_test_progress(course, username, test_id)
	if test_progress == None:
		messages.success(request, 'V tuto chvíli nemáš žádné dostupné testy')
		return redirect('tests:overview', course=course)

	if test_progress.state != TestState.CLOSE.value:
		messages.error(request, 'Nevalidní akce')
		return redirect('tests:overview', course=course)

	project = get_project_by_id(project_id, course)
	if project == None:
		messages.error(request, 'Pokus o odemknutí neexistujícího testu')
		return redirect('tests:overview', course=course)

	test_data, _ = get_test(course, test_id)
	if test_data == None:
		messages.error(request, 'Pokus o odemknutí neexistujícího testu')
		return redirect('tests:overview', course=course)

	chapter = get_chapter_by_id(test_data.finish_chapter, course, project.database)
	if chapter == None:
		messages.error(request, 'Pokus o odemknutí neexistujícího testu')
		return redirect('tests:overview', course=course)

	if is_chapter_open(username, course, project.id, chapter.lesson_id, chapter.id):
		unlock_test(course, username, test_data.id, TestState.OPEN)
		return redirect('tests:overview', course=course)
	else:
		messages.error(request, 'Test není možné odemknout')
		return redirect('courses:overview')


@login_required
def display_test(request: HttpRequest, course: str, test_id: int) -> HttpResponse:
	"""display one test"""
	username = request.user.username #type: ignore

	test_progress = get_test_progress(course, username, test_id)
	if test_progress == None or test_progress.state == TestState.CLOSE.value:
		messages.error(request, 'Nevalidní akce')
		return redirect('tests:overview', course=course)

	if test_progress.attempts == 0:
		messages.error(request, 'Nevalidní akce')
		return redirect('tests:overview', course=course)

	test_data, questionDataCollection = get_test(course, test_id)
	if test_data == None or questionDataCollection == None:
		messages.error(request, 'Pokus o přístup k neexistujícímu testu')
		return  redirect('tests:overview', course=course, sort_type='all')

	return render(request, 'tests/detail.html', {
		'testForm': DynamicTestForm(questionDataCollection),
		'course': course,
		'test': test_data,
		'test_attempts': test_progress.attempts,
	})


@login_required
def validate_test(request: HttpRequest, course: str, test_id: int) -> HttpResponse:
	"""validate one test"""
	username = request.user.username #type: ignore
	test_data, questionDataCollection = get_test(course, test_id)

	if test_data == None or questionDataCollection == None:
		messages.error(request, 'Pokus o přístup k neexistujícímu testu')
		return  redirect('tests:overview', course=course, sort_type='all')

	test_result, test_happened =  validate_test_get_result(request.POST, test_data, questionDataCollection, course, username, test_id)
	if not test_happened:
		messages.error(request, 'Nevalidní akce')
		return  redirect('tests:overview', course=course, sort_type='all')

	return  redirect('tests:result', course=course, sort_type='all', test_id=test_data.id)


@login_required
def results(request: HttpRequest, course: str, test_id: int)  -> HttpResponse:
	"""list all projects"""
	username = request.user.username #type: ignore

	test_data, _ = get_test(course, test_id)
	if test_data == None:
		messages.error(request, 'Pokus o přístup k neexistujícímu testu')
		return  redirect('tests:overview', course=course, sort_type='all')

	test_progress = get_test_progress(course, username, test_id)
	if test_progress == None:
		messages.success(request, 'Zatím u testu nejsou žádné výsledky')
		return redirect('tests:overview', course=course)

	if test_progress.state == TestState.CLOSE.value:
		messages.error(request, 'Nevalidní akce')
		return redirect('tests:overview', course=course)

	return render(request, 'tests/results.html', {
		'course': course,
		'test_progress': test_progress,
		'test_data': test_data,
	})


