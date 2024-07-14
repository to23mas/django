from django import forms


class ProjectEditForm(forms.Form):

	no = forms.IntegerField()
	title = forms.CharField()
	projects = forms.CharField()
	description = forms.CharField(
		widget=forms.Textarea(attrs={'rows': 5}),
	)
	todo = forms.CharField(
		widget=forms.Textarea(attrs={'rows': 5}),
	)

	def clean_todo(self):
		data = self.cleaned_data['todo']
		string_list = [s.strip() for s in data.split(',') if s.strip()]
		return string_list

