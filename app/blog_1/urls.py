from django.urls import path
from . import views

app_name = 'blog_1'

urlpatterns = [
	path('posts', views.post_list, name='post_list'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	path('post/create/', views.post_create, name='post_create'),
	path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
	path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),

	path('categories', views.category_list, name='category_list'),
	path('category/<int:pk>/', views.category_detail, name='category_detail'),
	path('category/create/', views.category_create, name='category_create'),
	path('category/<int:id>/edit/', views.category_edit, name='category_edit'),
	path('category/<int:id>/delete/', views.category_delete, name='category_delete'),
]
