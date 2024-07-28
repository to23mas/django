from django import forms


class ProjectEditForm(forms.Form):

	id = forms.IntegerField(required=False)
	title = forms.CharField()
	database = forms.CharField()
	description = forms.CharField(
		required=False,
		widget=forms.Textarea(attrs={'rows': 5}),
	)
	todo = forms.CharField(
		required=False,
		widget=forms.Textarea(attrs={'rows': 5}),
	)

	def get_todo_as_string(self):
		todo_list = self.cleaned_data.get('todo', [])
		return ', '.join(todo_list)

	def __init__(self, *args, **kwargs):
		initial = kwargs.get('initial', {})
		if 'todo' in initial and isinstance(initial['todo'], list):
			initial['todo'] = ', '.join(initial['todo'])
		kwargs['initial'] = initial
		super(ProjectEditForm, self).__init__(*args, **kwargs)

		self.fields['id'].widget.attrs['readonly'] = True

		if initial:
			self.fields['database'].widget.attrs['readonly'] = True
			self.fields['id'].initial = initial['_id']
