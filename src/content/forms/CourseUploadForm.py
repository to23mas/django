from django import forms

class CourseUploadForm(forms.Form):
	file = forms.FileField()
