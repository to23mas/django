from django.urls import path
from . import views

app_name = 'habit_tracker_2'

urlpatterns = [
	path('2/', views.habit_tracker, name="habit_tracker"),
	path('2/complete-habit/<int:habit_id>/', views.complete_habit, name='complete_habit'),
	path('delete/<int:habit_id>/', views.delete_habit, name='delete_habit'),
]
