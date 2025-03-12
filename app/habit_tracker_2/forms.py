from django import forms
from habit_tracker_1.models import Habit


class HabitForm(forms.ModelForm):
	class Meta:
		model = Habit
		fields = ['name']  # Only include the 'name' field in the form
		widgets = {
			'name': forms.TextInput(attrs={
				'placeholder': 'Název zvyku',
				'class': 'habit_tracker_input_field',
		})}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['name'].label = False  # Disable label for the 'name' field
