from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from .schema import schema

from . import views
from . import demos
from .demos.library_jsonrpc import library_jsonrpc, jsonrpc_endpoint, reset_data_jsonrpc

app_name = 'demos'

urlpatterns = [
	path('overview/c-<str:course>/', views.overview, name='overview'),
	path('detail/c-<str:course>/demo-<int:demo_id>/', views.detail, name='detail'),

	#INDIVIDUAL DEMOS

	#hello world
	path('c-<str:course>/demo-<int:demo_id>/hello_world', demos.hello_world, name='hello_world'),

	#hangman
	path('c-<str:course>/demo-<int:demo_id>/hangman', demos.hangman, name='hangman'),

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
	#blog
	path('c-<str:course>/d-<int:demo_id>/posts', demos.blog_1, name='blog_1'),
	path('c-<str:course>/d-<int:demo_id>/post/<int:pk>/', demos.post_detail, name='post_detail'),
	path('c-<str:course>/d-<int:demo_id>/post/create/', demos.post_create, name='post_create'),
	path('c-<str:course>/d-<int:demo_id>/post/<int:pk>/edit/', demos.post_edit, name='post_edit'),
	path('c-<str:course>/d-<int:demo_id>/post/<int:pk>/delete/', demos.post_delete, name='post_delete'),
	path('c-<str:course>/d-<int:demo_id>/categories/', demos.category_list, name='category_list'),
	path('c-<str:course>/d-<int:demo_id>/category/<int:pk>/', demos.category_detail, name='category_detail'),
	path('c-<str:course>/d-<int:demo_id>/category/create/', demos.category_create, name='category_create'),
	path('c-<str:course>/d-<int:demo_id>/category/<int:id>/edit/', demos.category_edit, name='category_edit'),
	path('c-<str:course>/d-<int:demo_id>/category/<int:id>/delete/', demos.category_delete, name='category_delete'),
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

	# Library demo URLs - now just include the library_patterns
	path('c-<str:course>/d-<int:demo_id>/library/', demos.library, name='library'),
	path('c-<str:course>/d-<int:demo_id>/library/iframe/', demos.library_iframe, name='library_iframe'),
	path('c-<str:course>/d-<int:demo_id>/library/rest/', demos.library_rest_view, name='library_rest'),
	path('c-<str:course>/d-<int:demo_id>/library/api/books/', demos.api_books, name='api_books'),
	path('c-<str:course>/d-<int:demo_id>/library/api/books/<int:book_id>/', demos.api_book_detail, name='api_book_detail'),
	path('c-<str:course>/d-<int:demo_id>/library/api/reset/', demos.reset_data_rest, name='reset_data_rest'),

	# GraphQL endpoint
	path('c-<str:course>/d-<int:demo_id>/graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)), name='graphql'),
	path('c-<str:course>/d-<int:demo_id>/library/graphql/', demos.library_graphql, name='library_graphql'),
	path('c-<str:course>/d-<int:demo_id>/library/api/reset_graphql/', demos.reset_data_graph, name='reset_data_graph'),

	# JSON-RPC patterns
	path('c-<str:course>/d-<int:demo_id>/library/jsonrpc/', library_jsonrpc, name='library_jsonrpc'),
	path('c-<str:course>/d-<int:demo_id>/jsonrpc/', jsonrpc_endpoint, name='jsonrpc_endpoint'),
	path('c-<str:course>/d-<int:demo_id>/library/api/reset-jsonrpc/', reset_data_jsonrpc, name='reset_data_jsonrpc'),
]
