from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'completed', 'date_completed', 'completion_count')
    search_fields = ('name',)
    list_filter = ('completed', 'date_completed')
