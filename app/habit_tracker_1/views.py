from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Habit

def habit_tracker(request):
	if request.method == "POST":
		habit_name = request.POST.get("habit_name")  # Získání názvu z formuláře
		if habit_name:  # Ověření, že není prázdný
			Habit.objects.create(name=habit_name)
			return redirect('habit_tracker_1:habit_tracker')

	_reset_progress()
	habits = Habit.objects.all()
	return render(request, 'habit_tracker_1/habit_tracker.html', {'habits': habits})

def complete_habit(request, habit_id):
	habit = Habit.objects.get(id=habit_id)
	habit.completed = True
	habit.date_completed = timezone.now().date()  # Nastaví dnešní datum
	habit.completion_count += 1  # Zvýší počet splnění o 1
	habit.save()

	_reset_progress()

	return redirect('habit_tracker_1:habit_tracker')


def delete_habit(request, habit_id):
	habit = Habit.objects.get(id=habit_id)
	habit.delete()

	return redirect('habit_tracker_1:habit_tracker')

def _reset_progress():
	current_date = timezone.now().date()
	habits = Habit.objects.all()

	for habit in habits:
		if habit.date_completed != current_date:
			habit.completion_count = 0
			habit.date_completed = None
			habit.save()
