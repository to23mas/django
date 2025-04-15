from django.contrib import admin
from .models import TestResult

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('test_id', 'question_id', 'question_type', 'attempt_number', 'is_correct', 'is_partially_correct')
    list_filter = ('test_id', 'question_id', 'question_type', 'attempt_number', 'is_correct', 'is_partially_correct')
    search_fields = ('test_id', 'question_id')
    readonly_fields = ('test_id', 'question_id', 'question_type', 'attempt_number')
    ordering = ('test_id', 'question_id', 'attempt_number')
