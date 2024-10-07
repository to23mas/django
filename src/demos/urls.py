from django.urls import path

from . import views
from .import demos

app_name = 'demos'
urlpatterns = [
	path('overview/c-<str:course>/', views.overview, name='overview'),
	path('detail/c-<str:course>/demo-<int:demo_id>/', views.detail, name='detail'),

	#Individual demos
	path('detail/c-<str:course>/demo-<int:demo_id>/hello_world', demos.hello_world, name='hello_world'),
]
