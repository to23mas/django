from django import forms


class LessonEditForm(forms.Form):
	id = forms.IntegerField(required=False)
	title = forms.CharField()
	to = forms.CharField(
		required=False,
		widget=forms.Textarea(attrs={'rows': 5}),
	)


	def __init__(self, *args, **kwargs):
		initial = kwargs.get('initial', {})
		kwargs['initial'] = initial
		if 'to' in initial and isinstance(initial['to'], list):
			initial['to'] = ', '.join(initial['to'])
		super(LessonEditForm, self).__init__(*args, **kwargs)

		if initial:
			self.fields['id'].initial = initial['_id']
		self.fields['id'].widget.attrs['readonly'] = True


	def get_to_as_string(self):
		to_list = self.cleaned_data.get('to', [])
		return ', '.join(to_list)


	def clean_to(self):
		data = self.cleaned_data['to']
		if isinstance(data, str):
			string_list = [s.strip() for s in data.split(',') if s.strip()]
		else:
			string_list = [str(data).strip()]

		return string_list
