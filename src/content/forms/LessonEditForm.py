from django import forms

from domain.data.projects.ProjectStorage import find_projects


class LessonEditForm(forms.Form):
	no = forms.IntegerField()
	title = forms.CharField()
	project = forms.ChoiceField(widget=forms.Select)

	def __init__(self, *args, db=None, **kwargs):
		initial = kwargs.get('initial', {})
		kwargs['initial'] = initial
		super(LessonEditForm, self).__init__(*args, **kwargs)

		if db:
			self.fields['project'].choices = [(int(project.no), project.title) for project in find_projects(db)]
		if initial:
			self.fields['no'].widget.attrs['disabled'] = True
