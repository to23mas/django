"""URLS"""
from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project-<int:project_id>/lesson-<int:lesson_id>/chapter-<int:chapter_id>', views.lesson, name='lesson'),
    path('lesson/next-chapter', views.next_chapter, name='next_chapter'),
    path('lesson/unclock-chapter', views.unlock_chapter, name='unlock_chapter'),
]
