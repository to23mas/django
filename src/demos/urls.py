from django.urls import path

from . import views
from . import demos

app_name = 'demos'
urlpatterns = [
	path('overview/c-<str:course>/', views.overview, name='overview'),
	path('detail/c-<str:course>/demo-<int:demo_id>/', views.detail, name='detail'),

	#INDIVIDUAL DEMOS

	#hello world
	path('c-<str:course>/demo-<int:demo_id>/hello_world', demos.hello_world, name='hello_world'),

	#habit_tracker_1
	path('c-<str:course>/demo-<int:demo_id>/h_t_1', demos.h_t_1, name='h_t_1'), #parent html containing iframe
	path('c-<str:course>/demo-<int:demo_id>/h_t_1/iframe', demos.habit_tracker_1, name='habit_tracker_1'),
	path('c-<str:course>/demo-<int:demo_id>/h_t_1/c/<str:habit_name>/iframe', demos.complete_habit_1, name='complete_habit_1'),
	path('c-<str:course>/demo-<int:demo_id>/h_t_1/d/<str:habit_name>/iframe', demos.delete_habit_1, name='delete_habit_1'),
	path('c-<str:course>/demo-<int:demo_id>/h_t_1/clear_session', demos.clear_session_1, name='clear_session_1'),
	#habit_tracker_2
	path('detail/c-<str:course>/demo-<int:demo_id>/h_t_2', demos.h_t_2, name='h_t_2'),
	path('detail/c-<str:course>/demo-<int:demo_id>/h_t_2/c/<str:habit_name>', demos.complete_habit_2, name='complete_habit_2'),
	path('detail/c-<str:course>/demo-<int:demo_id>/h_t_2/d/<str:habit_name>', demos.delete_habit_2, name='delete_habit_2'),
	path('detail/c-<str:course>/demo-<int:demo_id>/h_t_2/clear_session', demos.clear_session_2, name='clear_session_2'),
]
