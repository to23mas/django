from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def overview(request: HttpRequest, course: str, sort_type: str) -> HttpResponse:
    """list all projects"""

    # test_progress =
    #TODO -> displaty all tests
    return render(request, 'tests/overview.html', {
        # 'projects': projects_collection,
        # 'user_progress': user_progress,
        'course_name': course,
    })
