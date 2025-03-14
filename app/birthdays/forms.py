from django import forms
from django.core.exceptions import ValidationError
from .models import Birthday

class BirthdayForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_attrs = {'class': 'block text-sm font-medium text-gray-700 mb-2'}

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        birth_date = cleaned_data.get('birth_date')

        if name and birth_date:
            if Birthday.objects.filter(name=name, birth_date=birth_date).exists():
                raise ValidationError('A birthday entry with this name and date already exists.')
        return cleaned_data

    class Meta:
        model = Birthday
        fields = ['calendar_name', 'name', 'birth_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter name'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500'
            }),
            'calendar_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter calendar name'
            })
        } 