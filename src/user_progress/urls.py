"""URLS"""
from django.urls import path

from . import views
from . import validator
from . import cli

app_name = 'user_progress'

urlpatterns = [

	path('lesson/next-chapter', views.next_chapter, name='next_chapter'),
	path('lesson/unlock-chapter', views.unlock_next_chapter, name='unlock_chapter'),
	path('lesson/validate-python', validator.validate_python, name='validate_python'),
	path('lesson/validate-cli', cli.validate_cli, name='validate_cli'),
]
