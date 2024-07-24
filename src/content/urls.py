from django.urls import path

from .views import *


urlpatterns = [
	path('', course_overview, name='admin_course_overview'),

	path('course/<str:course_id>/edit', course_edit, name='admin_course_edit'),
	path('course/<str:course_id>/delete', course_delete, name='admin_course_delete'),
	path('course/new', course_new, name='admin_course_new'),

	path('course/<str:course_id>/projects', project_overview, name='admin_project_overview'),
	path('course/<str:course_id>/projects/<int:project_id>/edit', project_edit, name='admin_project_edit'),
	path('course/<str:course_id>/projects/new', project_new, name='admin_project_new'),
	path('course/<str:course_id>/projects/<str:project_id>/delete', project_delete, name='admin_project_delete'),

	path('course/<str:course_id>-<int:project_id>/lessons', lesson_overview, name='admin_lesson_overview'),
	path('course/<str:course_id>-<int:project_id>/lessons/new', lesson_new, name='admin_lesson_new'),
	path('course/<str:course_id>-<int:project_id>-<int:lesson_id>/lessons/edit', lesson_edit, name='admin_lesson_edit'),
	path('course/<str:course_id>-<int:project_id>-<int:lesson_id>/lessons/delete', lesson_delete, name='admin_lesson_delete'),

	path('course/<str:course_id>-<int:project_id>/chapters', chapter_overview, name='admin_chapter_overview'),
	path('course/<str:course_id>-<int:project_id>/chapters/new', chapter_new, name='admin_chapter_new'),
	path('course/<str:course_id>-<int:project_id>-<int:lesson_id>-<int:chapter_id>/chapters/edit', chapter_edit, name='admin_chapter_edit'),
	path('course/<str:course_id>-<int:project_id>-<int:lesson_id>-<int:chapter_id>/chapters/delete', chapter_delete, name='admin_chapter_delete'),

	path('course/<str:course_id>/tests', test_overview, name='admin_test_overview'),
    path('course/<str:course_id>-<int:test_id>/test/edit', test_edit, name='admin_test_edit'),
]
