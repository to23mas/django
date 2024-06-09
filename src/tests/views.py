from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.progress_storage import find_available_tests, find_tests_progress
from domain.data.tests_storage import find_tests_for_overview, get_test


@login_required
def overview(request: HttpRequest, course: str, sort_type: str) -> HttpResponse:
    """list of all available tests"""

    # TODO -> implement sort_type
    username = request.user.username #type: ignore

    user_tests_progress = find_tests_progress(course, username)
    user_available = find_available_tests(course, username)
    if user_available == None:
        messages.success(request, 'V tuto chvíli nemáš žádné dostupné testy')
        return render(request, 'tests/overview.html', {
            'course_name': course,
        })

    available_tests = find_tests_for_overview(course, user_available)

    return render(request, 'tests/overview.html', {
        'tests': available_tests,
        'progress': user_tests_progress,
        'course_name': course,
    })


@login_required
def detail(request: HttpRequest, course: str, test_no: str) -> HttpResponse:
    """display one test"""

    username = request.user.username #type: ignore
    user_tests_progress = find_tests_progress(course, username)

    test = get_test(course, test_no)
    if test == None:
        messages.success(request, 'Pokus o přístup k neexistujícímu testu')
        return  redirect('tests:overview', course=course, sort_type='all')


    #TODO -> displaty all tests
    return render(request, 'tests/detail.html', {
        'test': test,
        # 'progress': user_tests_progress, # TODO -> pro testy, které uživatel opakuje asi změnit vizuál + display pokus
        'course_name': course,
    })

@login_required
def results(request: HttpRequest, course: str, sort_type: str) -> HttpResponse:
    """list all projects"""
    pass

