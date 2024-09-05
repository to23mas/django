from django.urls import path

from .views import *
from .demos import *

app_name = 'demos'
urlpatterns = [
	path('overview/c-<str:course>/', overview, name='overview'),
	path('detail/c-<str:course>/demo-<int:demo_id>/', detail, name='detail'),


	#Individual demos
	path('detail/c-<str:course>/demo-<int:demo_id>/hello_world', hello_world, name='hello_world'),
]
