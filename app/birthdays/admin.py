from django.contrib import admin
from .models import Birthday

@admin.register(Birthday)
class BirthdayAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'created_at')
    search_fields = ('name',)
    list_filter = ('birth_date',)
