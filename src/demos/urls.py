from django.urls import path

from . import views
from .import demos

app_name = 'demos'
urlpatterns = [
	path('overview/c-<str:course>/', views.overview, name='overview'),
	path('detail/c-<str:course>/demo-<int:demo_id>/', views.detail, name='detail'),

	#Individual demos
	#hello world
	path('detail/c-<str:course>/demo-<int:demo_id>/hello_world', demos.parent_page, name='hello_world'),
	#habit_tracker_1
	path('detail/c-<str:course>/demo-<int:demo_id>/h_t_1', demos.hello_world, name='parent_page'),
	path('detail/c-<str:course>/demo-<int:demo_id>/h_t_1/iframe', demos.hello_world, name='habit_tracker_1'),
	path('detail/c-<str:course>/demo-<int:demo_id>/h_t_1/c/<str:habit_name>/iframe', demos.complete_habit_1, name='complete_habit_1'),
	path('detail/c-<str:course>/demo-<int:demo_id>/h_t_1/d/<str:habit_name>/iframe', demos.delete_habit_1, name='delete_habit_1'),
	path('detail/c-<str:course>/demo-<int:demo_id>/h_t_1/clear_session', demos.clear_session, name='clear_session'),
]
