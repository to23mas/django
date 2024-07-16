from django.urls import path

from .views import *


urlpatterns = [
	path('', course_overview, name='admin_course_overview'),
	path('course/<str:course_id>', course_edit, name='admin_course_edit'),
	path('course/<str:course_id>/projects', project_overview, name='admin_project_overview'),
	path('course/<str:course_id>/projects/<str:project_no>/edit', project_edit, name='admin_project_edit'),
	path('course/<str:course_id>/lessons', lesson_overview, name='admin_lesson_overview'),
	path('course/<str:course_id>/lessons/<str:project_no>-<str:lesson_no>', lesson_edit, name='admin_lesson_edit'),
	path('course/<str:course_id>/chapters', chapter_overview, name='admin_chapter_overview'),
	path('course/<str:course_id>/chapters/<str:project_no>-<str:lesson_no>-<str:chapter_no>', chapter_edit, name='admin_chapter_edit'),
	path('course/<str:course_id>/tests', test_overview, name='admin_test_overview'),
    path('course/<str:course_id>/tests/<str:test_no>', test_edit, name='admin_test_edit'),
]
