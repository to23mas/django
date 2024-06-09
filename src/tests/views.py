from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from domain.data.progress_storage import find_available_tests, find_tests_progress
from domain.data.tests_storage import find_tests


@login_required
def overview(request: HttpRequest, course: str, sort_type: str) -> HttpResponse:
    """list all projects"""

    username = request.user.username #type: ignore

    all_tests = find_tests(course)
    user_tests_progress = find_tests_progress(course, username)
    user_avail = find_available_tests(course, username)
    avail_tests = find_tests(course, user_avail)

    #TODO -> displaty all tests
    return render(request, 'tests/overview.html', {
        # 'projects': projects_collection,
        'tests': list(avail_tests),
        'progress': user_tests_progress,
        'avail': user_avail,
        'course_name': course,
    })
