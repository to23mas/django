from django.urls import path
from . import views

app_name = 'birthdays'

urlpatterns = [
    path('', views.birthday_list, name='birthday_list'),
    path('delete/<int:birthday_id>/', views.delete_birthday, name='delete_birthday'),
    path('test-email/', views.test_birthday_email, name='test_email'),
    path('cron/<str:action>/', views.manage_cron, name='manage_cron'),
]