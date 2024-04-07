"""URLS"""
from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('lesson-<int:lesson_id>/chapter-<int:chapter_id>', views.lesson, name='lesson'),
]
