from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpRequest, HttpResponse

from domain.data.chapters.ChapterStorage import ChapterStorage
from domain.data.progress.ProgressStorage import ProgressStorage
from domain.data.projects.ProjectStorage import ProjectStorage
from domain.data.tests.TestStorage import TestStorage

from domain.data.tests.enum.TestState import TestState
from domain.data.tests_progress.TestProgressStorage import TestProgressStorage
from tests.forms import DynamicTestForm
from tests.utils import reset_test_lock_time, validate_test_get_result


@login_required
def overview(request: HttpRequest, course: str) -> HttpResponse:
	"""list of all available tests"""

	username = request.user.username #type: ignore
	user_available = ProgressStorage().find_available_tests(course, username)

	if user_available is None or len(user_available) == 0:
		messages.success(request, 'V tuto chvíli nemáš žádné dostupné testy')
		return render(request, 'tests/overview.html', {
			'course': course,
		})

	available_tests = TestStorage().find_tests_for_overview(course, user_available)

	for test in available_tests:
		reset_test_lock_time(
			TestProgressStorage().get_test_progress(course, username, test.id), #type: ignore
			course,
			username,
			test,
		)

	return render(request, 'tests/overview.html', {
		'tests': available_tests,
		'course': course,
		'username': username,
	})


def unlock(request: HttpRequest, course: str, test_id: int, project_id: int) -> HttpResponse:
	"""list of all available tests"""
	username = request.user.username #type: ignore

	test_progress = TestProgressStorage().get_test_progress(course, username, test_id)
	if test_progress is None:
		messages.success(request, 'V tuto chvíli nemáš žádné dostupné testy')
		return redirect('tests:overview', course=course)

	if test_progress.state != TestState.CLOSE.value:
		messages.error(request, 'Nevalidní akce')
		return redirect('tests:overview', course=course)

	project = ProjectStorage().get_project_by_id(project_id, course)
	if project is None:
		messages.error(request, 'Pokus o odemknutí neexistujícího testu')
		return redirect('tests:overview', course=course)

	test_data, _ = TestStorage().get_test(course, test_id)
	if test_data is None:
		messages.error(request, 'Pokus o odemknutí neexistujícího testu')
		return redirect('tests:overview', course=course)

	chapter = ChapterStorage().get_chapter_by_id(test_data.finish_chapter, course, project.database)
	if chapter is None:
		messages.error(request, 'Pokus o odemknutí neexistujícího testu')
		return redirect('tests:overview', course=course)

	if ProgressStorage().is_chapter_open(username, course, project.id, chapter.lesson_id, chapter.id):
		TestProgressStorage().unlock_test(course, username, test_data.id, TestState.OPEN)
		return redirect('tests:overview', course=course)

	messages.error(request, 'Test není možné odemknout')
	return redirect('courses:overview')


@login_required
def display_test(request: HttpRequest, course: str, test_id: int) -> HttpResponse:
	"""display one test"""
	username = request.user.username #type: ignore

	test_progress = TestProgressStorage().get_test_progress(course, username, test_id)
	if test_progress is None or test_progress.state is TestState.CLOSE.value:
		messages.error(request, 'Nevalidní akce')
		return redirect('tests:overview', course=course)

	if test_progress.attempts == 0:
		messages.error(request, 'Nevalidní akce')
		return redirect('tests:overview', course=course)

	test_data, questionDataCollection = TestStorage().get_test(course, test_id)
	if test_data is None or questionDataCollection is None:
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
	test_data, questionDataCollection = TestStorage().get_test(course, test_id)

	if test_data is None or questionDataCollection is None:
		messages.error(request, 'Pokus o přístup k neexistujícímu testu')
		return  redirect('tests:overview', course=course, sort_type='all')

	test_progress, test_happened = validate_test_get_result(request.POST, test_data, questionDataCollection, course, username, test_id)
	if not test_happened:
		messages.error(request, 'Nevalidní akce')
		return  redirect('tests:overview', course=course, sort_type='all')

	match (test_progress.success):
		case True: messages.success(request, f'Test úspěšně splněn na {test_progress.score_percentage:.2f}%')
		case False: messages.warning(request, f'Nebylo dosaženo požadovaného minima. Dosažené skóre: {test_progress.score_percentage:.2f}%')

	return  redirect('tests:results', course=course, test_id=test_data.id)


@login_required
def results(request: HttpRequest, course: str, test_id: int)  -> HttpResponse:
	"""list all projects"""
	username = request.user.username #type: ignore

	test_data, _ = TestStorage().get_test(course, test_id)
	if test_data is None:
		messages.error(request, 'Pokus o přístup k neexistujícímu testu')
		return  redirect('tests:overview', course=course, sort_type='all')

	test_progress = TestProgressStorage().get_test_progress(course, username, test_id)
	if test_progress is None:
		messages.success(request, 'Zatím u testu nejsou žádné výsledky')
		return redirect('tests:overview', course=course)

	if test_progress.state == TestState.CLOSE.value:
		messages.error(request, 'Nevalidní akce')
		return redirect('tests:overview', course=course)

	return render(request, 'tests/results.html', {
		'course': course,
		'test_progress': test_progress,
		'test_data': test_data,
		'last_percentage': f'{(test_progress.score[-1] / (test_data.total_points/100)):.2f}',
		'best_score': max(test_progress.score),
		'best_score_percentage': f'{(max(test_progress.score) / (test_data.total_points/100)):.2f}',
		'total_attempts': len(test_progress.score)
	})

