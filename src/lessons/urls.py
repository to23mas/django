"""URLS"""
from django.urls import path

from . import views

app_name = 'lessons'

urlpatterns = [
	path(
		'c-<str:course>/project-<int:project_id>/lesson-<int:lesson_id>/chapter-<int:chapter_id>',
		views.lesson,
		name='lesson'
	),
]
