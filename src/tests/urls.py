from django.urls import path

from .views import *

app_name = 'tests'
urlpatterns = [
    path('c-<str:course>/tests-<str:sort_type>/', overview, name='overview'),
]
