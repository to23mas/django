from typing import List
from django import forms


class CourseEditForm(forms.Form):


	order = forms.IntegerField()
	no = forms.IntegerField()
	title = forms.CharField()
	projects = forms.CharField()
	visible = forms.BooleanField()
	open = forms.BooleanField()
	description = forms.CharField(
		widget=forms.Textarea(attrs={'rows': 15}),  # Adjust rows as needed
	)
	tags = forms.CharField(
		widget=forms.Textarea(attrs={'rows': 5}),  # Adjust rows as needed
	)

	def clean_tags(self):
		data = self.cleaned_data['tags']
		string_list = [s.strip() for s in data.splitlines() if s.strip()]
		return string_list

