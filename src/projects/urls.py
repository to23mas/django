"""URLS"""
from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('project/<int:project_no>/', views.project_detail, name='project_detail'),
]
