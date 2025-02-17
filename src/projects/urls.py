"""URLS"""
from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
	path('c-<str:course>/overview-<str:sort_type>/', views.overview, name='overview'),
	path('c-<str:course>/project/<int:project_id>/', views.detail, name='detail'),
]
