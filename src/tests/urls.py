from django.urls import path

from .views import *

app_name = 'tests'
urlpatterns = [
	path('overview/c-<str:course>/', overview, name='overview'),
	path('unlock/c-<str:course>/tests-<int:test_id>-<int:project_id>/', unlock, name='unlock'),
	path('detail/c-<str:course>/tests-<int:test_id>/', display_test, name='test'),
	path('validate/c-<str:course>/tests-<int:test_id>/', validate_test, name='validate_test'),
	path('result/c-<str:course>/tests-<int:test_id>/', results, name='results'),
]
