from django.urls import path
from django.contrib.auth.views import LogoutView

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
	path('c-<str:course>/d-<int:demo_id>/h_t_1', demos.h_t_1, name='h_t_1'), #parent html containing iframe
	path('c-<str:course>/d-<int:demo_id>/h_t_1/iframe', demos.habit_tracker_1, name='habit_tracker_1'),
	path('c-<str:course>/d-<int:demo_id>/h_t_1/c/<str:habit_name>/iframe', demos.complete_habit_1, name='complete_habit_1'),
	path('c-<str:course>/d-<int:demo_id>/h_t_1/d/<str:habit_name>/iframe', demos.delete_habit_1, name='delete_habit_1'),
	path('c-<str:course>/d-<int:demo_id>/h_t_1/clear_session', demos.clear_session_1, name='clear_session_1'),
	#habit_tracker_2
	path('c-<str:course>/d-<int:demo_id>/h_t_2', demos.h_t_2, name='h_t_2'),
	path('c-<str:course>/d-<int:demo_id>/h_t_2/c/<str:habit_name>', demos.complete_habit_2, name='complete_habit_2'),
	path('c-<str:course>/d-<int:demo_id>/h_t_2/d/<str:habit_name>', demos.delete_habit_2, name='delete_habit_2'),
	path('c-<str:course>/d-<int:demo_id>/h_t_2/clear_session', demos.clear_session_2, name='clear_session_2'),
	#blog_1
	path('c-<str:course>/d-<int:demo_id>/b-1/posts', demos.blog_1, name='blog_1'),
	path('c-<str:course>/d-<int:demo_id>/b-1/post/<int:pk>/', demos.post_detail, name='post_detail'),
	path('c-<str:course>/d-<int:demo_id>/b-1/post/create/', demos.post_create, name='post_create'),
	path('c-<str:course>/d-<int:demo_id>/b-1/post/<int:pk>/edit/', demos.post_edit, name='post_edit'),
	path('c-<str:course>/d-<int:demo_id>/b-1/post/<int:pk>/delete/', demos.post_delete, name='post_delete'),
	path('c-<str:course>/d-<int:demo_id>/b-1/categories/', demos.category_list, name='category_list'),
	path('c-<str:course>/d-<int:demo_id>/b-1/category/<int:pk>/', demos.category_detail, name='category_detail'),
	path('c-<str:course>/d-<int:demo_id>/b-1/category/create/', demos.category_create, name='category_create'),
	path('c-<str:course>/d-<int:demo_id>/b-1/category/<int:id>/edit/', demos.category_edit, name='category_edit'),
	path('c-<str:course>/d-<int:demo_id>/b-1/category/<int:id>/delete/', demos.category_delete, name='category_delete'),
	#authentication
	path('c-<str:course>/d-<int:demo_id>/auth', demos.login, name='login'),
	path('auth/logout', LogoutView.as_view(), name='logout'),

	#administration
	path('c-<str:course>/d-<int:demo_id>/administration', demos.administration, name='administration'),

	#birthdays
    path('c-<str:course>/d-<int:demo_id>/birthdays/', demos.birthday, name='birthday'),
    path('c-<str:course>/d-<int:demo_id>/birthdays/delete/<int:pk>/', demos.delete_birthday, name='delete_birthday'),

	#chat
    path('c-<str:course>/d-<int:demo_id>/chat', demos.chat, name='room'),
]
