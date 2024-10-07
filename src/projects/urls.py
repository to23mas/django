"""URLS"""
from django.urls import path

from projects.views.chapters import next_chapter, unlock_next_chapter
from projects.views.lessons import lesson
from projects.views.projects import detail, overview
from projects.views.validator import validate_python

app_name = 'projects'

urlpatterns = [
	path('c-<str:course>/overview-<str:sort_type>/', overview, name='overview'),
	path('c-<str:course>/project/<int:project_id>/', detail, name='detail'),
	path('c-<str:course>/project-<int:project_id>/lesson-<int:lesson_id>/chapter-<int:chapter_id>', lesson, name='lesson'),
	path('lesson/next-chapter', next_chapter, name='next_chapter'),
	path('lesson/unlock-chapter', unlock_next_chapter, name='unlock_chapter'),
	path('lesson/validate-python', validate_python, name='validate_python'),
]
