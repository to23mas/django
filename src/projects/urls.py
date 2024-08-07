"""URLS"""
from django.urls import path
from .views import *

app_name = 'projects'

urlpatterns = [
	path('c-<str:course>/overview-<str:sort_type>/', overview, name='overview'),
	path('c-<str:course>/project/<int:project_id>/', detail, name='detail'),
	path('c-<str:course>/project-<int:project_id>/lesson-<int:lesson_id>/chapter-<int:chapter_id>', lesson, name='lesson'),
	path('lesson/next-chapter', next_chapter, name='next_chapter'),
	path('lesson/unclock-chapter', unlock_next_chapter, name='unlock_chapter'),
]
