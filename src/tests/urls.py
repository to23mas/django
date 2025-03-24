from django.urls import path

from tests.views import display_test, overview, results, unlock, validate_test, force_fail_test

app_name = 'tests'
urlpatterns = [
	path('overview/c-<str:course>/', overview, name='overview'),
	path('unlock/c-<str:course>/tests-<int:test_id>-<int:project_id>/', unlock, name='unlock'),
	path('detail/c-<str:course>/tests-<int:test_id>/', display_test, name='test'),
	path('validate/c-<str:course>/tests-<int:test_id>/', validate_test, name='validate_test'),
	path('result/c-<str:course>/tests-<int:test_id>/', results, name='results'),
	path('force-fail/<str:course>/<int:test_id>/', force_fail_test, name='force_fail_test'),
]
