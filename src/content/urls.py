from django.urls import path

from .views import *


urlpatterns = [
	path('', course_overview, name='admin_course_overview'),
	path('<str:course_no>/edit', course_edit, name='admin_course_edit'),
	path('<str:course_no>/projects', project_overview, name='admin_project_overview'),
	path('<str:course_no>/lessons', lesson_overview, name='admin_lesson_overview'),
	path('<str:course_no>/chapters', chapter_overview, name='admin_chapter_overview'),
	path('<str:course_no>/tests', test_overview, name='admin_test_overview'),
	path('<str:course_no>/projects/<str:project_no>/edit', project_edit, name='admin_project_edit'),
	path('<str:course_no>/lessons/<str:project_no>-<str:lesson_no>',
	  lesson_edit, name='admin_lesson_edit'),
]
