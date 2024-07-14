from django.urls import path

from .views import overview, TestDetailView

app_name = 'tests'
urlpatterns = [
	path('overview/c-<str:course>/', overview, name='overview'),
	path('detail/c-<str:course>/tests-<str:test_no>/', TestDetailView.as_view(), name='test'),
]
