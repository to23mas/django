from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from domain.data.courses_storage import find_courses


@login_required
def overview(request: HttpRequest) -> HttpResponse:
    """list all courses"""

    return render(request, 'courses/overview.html', {
        'courses': find_courses(),
        'courses_overview': True,
    })
