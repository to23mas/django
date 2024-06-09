from django.urls import path

from .views import *

app_name = 'tests'
urlpatterns = [
    path('overview/c-<str:course>/tests-<str:sort_type>/', overview, name='overview'),
    path('detail/c-<str:course>/tests-<str:test_no>/', detail, name='detail'),
]
