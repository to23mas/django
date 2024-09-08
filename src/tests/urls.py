from django.urls import path

from .views import overview, TestDetailView, unlock

app_name = 'tests'
urlpatterns = [
	path('overview/c-<str:course>/', overview, name='overview'),
	path('unlock/c-<str:course>/tests-<int:test_id>-<int:project_id>/', unlock, name='unlock'),
	path('detail/c-<str:course>/tests-<int:test_id>/', TestDetailView.as_view(), name='test'),
]
