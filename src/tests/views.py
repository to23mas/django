from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from domain.data.chapters.ChapterStorage import get_chapter, get_chapter_by_id
from domain.data.progress.ProgressStorage import find_available_tests, is_chapter_done, is_chapter_open
from domain.data.projects.ProjectStorage import get_project_by_id
from domain.data.tests.TestResultSerializer import TestResultSerializer
from domain.data.tests.TestStorage import find_tests_for_overview, get_test


from domain.data.tests.enum.TestState import TestState
from domain.data.tests_progress.TestProgressStorage import get_test_progress, unlock_test, update_test_progress
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
		return render(request, 'tests/overview.html', {'course': course})

	if test_progress.state != TestState.CLOSE.value:
		messages.error(request, 'Nevalidní akce')
		return render(request, 'tests/overview.html', {'course': course})

	project = get_project_by_id(project_id, course)
	if project == None:
		messages.error(request, 'Pokus o odemknutí neexistujícího testu')
		return render(request, 'tests/overview.html', {'course': course})

	test_data, _ = get_test(course, test_id)
	if test_data == None:
		messages.error(request, 'Pokus o odemknutí neexistujícího testu')
		return render(request, 'tests/overview.html', {'course': course})

	chapter = get_chapter_by_id(test_data.source_id, course, project.database)
	if chapter == None:
		messages.error(request, 'Pokus o odemknutí neexistujícího testu')
		return render(request, 'tests/overview.html', {'course': course})

	if is_chapter_open(username, course, project.id, chapter.lesson_id, chapter.id):
		unlock_test(course, username, test_data.id, TestState.OPEN)
		return redirect('tests:overview', course=course)
	else:
		messages.error(request, 'Test není možné odemknout')
		return redirect('courses:overview')


class TestDetailView(LoginRequiredMixin, View):
	def get(self, request: HttpRequest, course: str, test_id: int) -> HttpResponse:
		"""display one test"""

		username = request.user.username #type: ignore
		testData, questionDataCollection = get_test(course, test_id)
		if testData == None or questionDataCollection == None:
			messages.success(request, 'Pokus o přístup k neexistujícímu testu')
			return  redirect('tests:overview', course=course, sort_type='all')

		return render(request, 'tests/detail.html', {
			'testForm': DynamicTestForm(questionDataCollection),
			'course': course,
		})


	def post(self, request: HttpRequest, course: str, test_id: int) -> HttpResponse:
		"""validate one test"""
		username = request.user.username #type: ignore
		test_data, questionDataCollection = get_test(course, test_id)

		if test_data == None or questionDataCollection == None:
			messages.success(request, 'Pokus o přístup k neexistujícímu testu')
			return  redirect('tests:overview', course=course, sort_type='all')

		test_result =  validate_test_get_result(request.POST, test_data, questionDataCollection, course, username, test_no)

		return JsonResponse({'test_result_data': TestResultSerializer.to_array(test_result)})

@login_required
def results(request: HttpRequest, course: str, sort_type: str) -> HttpResponse:
	"""list all projects"""
	pass

