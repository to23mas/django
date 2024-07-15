from typing import List
from django import forms


class CourseEditForm(forms.Form):


	id = forms.CharField()
	order = forms.IntegerField()
	no = forms.IntegerField()
	title = forms.CharField()
	database = forms.CharField()
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
		string_list = [s.strip() for s in data.split(',') if s.strip()]
		return string_list

	def __init__(self, *args, **kwargs):
		super(CourseEditForm, self).__init__(*args, **kwargs)
		self.fields['id'].widget.attrs['disabled'] = True
