from django.urls import path
from . import views

app_name = 'library_rest'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/books/', views.book_list, name='book_list'),
    path('api/books/<int:pk>/', views.book_detail, name='book_detail'),
    path('reset-data/', views.reset_data, name='reset_data'),
] 
