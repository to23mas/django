from django.urls import path

from .views import *


urlpatterns = [
	path('', course_overview, name='admin_course_overview'),
	path('course/<str:course_id>/edit', course_edit, name='admin_course_edit'),
	path('course/<str:course_id>/delete', course_delete, name='admin_course_delete'),
	path('course/new', course_new, name='admin_course_new'),
	path('course/<str:course_id>/projects', project_overview, name='admin_project_overview'),
	path('course/<str:course_id>/projects/<str:project_no>/edit', project_edit, name='admin_project_edit'),
	path('course/<str:course_id>/projects/new', project_new, name='admin_project_new'),
	path('course/<str:course_id>/projects/<str:project_no>/delete', project_delete, name='admin_project_delete'),
	path('course/<str:course_id>/lessons', lesson_overview, name='admin_lesson_overview'),
	path('course/<str:course_id>/lessons/new', lesson_new, name='admin_lesson_new'),
	path('course/<str:course_id>/lessons/<str:project_no>-<str:lesson_no>/edit', lesson_edit, name='admin_lesson_edit'),
	path('course/<str:course_id>/lessons/<str:project_no>-<str:lesson_no>/delete', lesson_delete, name='admin_lesson_delete'),
	path('course/<str:course_id>/chapters', chapter_overview, name='admin_chapter_overview'),
	path('course/<str:course_id>/chapters/<str:project_no>-<str:lesson_no>-<str:chapter_no>', chapter_edit, name='admin_chapter_edit'),
	path('course/<str:course_id>/tests', test_overview, name='admin_test_overview'),
    path('course/<str:course_id>/tests/<str:test_no>', test_edit, name='admin_test_edit'),
]
