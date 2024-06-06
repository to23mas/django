"""URLS"""
from django.urls import path
from . import views
from .viewss import overview

app_name = 'projects'
urlpatterns = [
    path('c-<str:course>/overview-<str:sort_type>/', overview, name='overview'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project-<int:project_id>/lesson-<int:lesson_id>/chapter-<int:chapter_id>', views.lesson, name='lesson'),
    path('lesson/next-chapter', views.next_chapter, name='next_chapter'),
    path('lesson/unclock-chapter', views.unlock_chapter, name='unlock_chapter'),
]
