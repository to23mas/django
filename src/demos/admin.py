from django.contrib import admin
from .models import Habit, Category, Post

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
	list_display = ('name', 'completed', 'date_completed', 'completion_count')
	list_filter = ('completed', 'date_completed')
	search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')
	search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'created_at', 'updated_at')
	list_filter = ('created_at', 'updated_at', 'categories')
	search_fields = ('title', 'content')
	filter_horizontal = ('categories',)
