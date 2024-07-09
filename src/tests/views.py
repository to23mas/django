from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from domain.data.progress_storage import find_available_tests
from domain.data.tests.TestResultSerializer import TestResultSerializer
from domain.data.tests.TestStorage import find_tests_for_overview, get_test


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
			'course_name': course,
		})

	available_tests = find_tests_for_overview(course, user_available)

	return render(request, 'tests/overview.html', {
		'tests': available_tests,
		'course': course,
		'username': username,
		'course_name': course,
	})


class TestDetailView(LoginRequiredMixin, View):
	def get(self, request: HttpRequest, course: str, test_no: str) -> HttpResponse:
		"""display one test"""

		username = request.user.username #type: ignore
		testData, questionDataCollection = get_test(course, test_no)
		if testData == None or questionDataCollection == None:
			messages.success(request, 'Pokus o přístup k neexistujícímu testu')
			return  redirect('tests:overview', course=course, sort_type='all')

		return render(request, 'tests/detail.html', {
			'testForm': DynamicTestForm(questionDataCollection),
			'course_name': course,
		})

	def post(self, request: HttpRequest, course: str, test_no: str) -> HttpResponse:
		"""validate one test"""
		username = request.user.username #type: ignore
		test_data, questionDataCollection = get_test(course, test_no)

		if test_data == None or questionDataCollection == None:
			messages.success(request, 'Pokus o přístup k neexistujícímu testu')
			return  redirect('tests:overview', course=course, sort_type='all')

		test_result =  validate_test_get_result(request.POST, test_data, questionDataCollection, course, username, test_no)

		return JsonResponse({'test_result_data': TestResultSerializer.to_array(test_result)})
		messages.warning(request, f'Nebylo dosaženo požadovaného minima')



@login_required
def results(request: HttpRequest, course: str, sort_type: str) -> HttpResponse:
	"""list all projects"""
	pass

