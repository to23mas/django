from django.urls import path
from . import views

app_name = 'habit_tracker_1'

urlpatterns = [
	path('1/', views.habit_tracker, name="habit_tracker"),
	path('1/complete-habit/<int:habit_id>/', views.complete_habit, name='complete_habit'),
	path('delete/<int:habit_id>/', views.delete_habit, name='delete_habit'),
]
