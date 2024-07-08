from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.progress_storage import find_available_tests, find_tests_progress
from domain.data.tests_progress.test_progress_storage import get_test_progress
from domain.data.tests_storage import find_tests_for_overview, get_test

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from tests.forms import DynamicTestForm
from tests.utils import progress_test


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
        user_tests_progress = find_tests_progress(course, username)

        print(get_test_progress(course, username, test_no))
        testData = get_test(course, test_no)
        if testData == None:
            messages.success(request, 'Pokus o přístup k neexistujícímu testu')
            return  redirect('tests:overview', course=course, sort_type='all')

        return render(request, 'tests/detail.html', {
            'testForm': DynamicTestForm(testData),
            # 'progress': user_tests_progress, # TODO -> pro testy, které uživatel opakuje asi změnit vizuál + display pokus
            'course_name': course,
        })

    def post(self, request: HttpRequest, course: str, test_no: str) -> HttpResponse:
        """validate one test"""
        username = request.user.username #type: ignore
        testData = get_test(course, test_no)

        if testData == None:
            messages.success(request, 'Pokus o přístup k neexistujícímu testu')
            return  redirect('tests:overview', course=course, sort_type='all')

        if (not progress_test(request.POST,  testData, course, username, test_no)):
            messages.success(request, f'Test úspěšně splněn')
            return  redirect('tests:overview', course=course, sort_type='all')

        messages.warning(request, f'Nebylo dosaženo požadovaného minima')



@login_required
def results(request: HttpRequest, course: str, sort_type: str) -> HttpResponse:
    """list all projects"""
    pass

