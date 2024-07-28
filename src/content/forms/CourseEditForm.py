from django import forms


class CourseEditForm(forms.Form):
	order = forms.IntegerField()
	id = forms.IntegerField(required=False)
	title = forms.CharField()
	database = forms.CharField()
	visible = forms.BooleanField(required=False, initial=False)
	open = forms.BooleanField(required=False, initial=False)
	description = forms.CharField(
		required=False,
		widget=forms.Textarea(attrs={'rows': 15}),
	)
	tags = forms.CharField(
		required=False,
		widget=forms.Textarea(attrs={'rows': 5}),
	)


	def clean_tags(self):
		data = self.cleaned_data['tags']
		string_list = [s.strip() for s in data.split(',') if s.strip()]
		return string_list


	def get_tags_as_string(self):
		tags_list = self.cleaned_data.get('tags', [])
		return ', '.join(tags_list)


	def __init__(self, *args, database=None, **kwargs):
		initial = kwargs.get('initial', {})
		if 'tags' in initial and isinstance(initial['tags'], list):
			initial['tags'] = ', '.join(initial['tags'])
		kwargs['initial'] = initial
		super(CourseEditForm, self).__init__(*args, **kwargs)

		self.fields['id'].widget.attrs['readonly'] = True
		if database:
			self.fields['database'].widget.attrs['readonly'] = True
			self.fields['database'].initial = database
		if initial:
			self.fields['database'].widget.attrs['readonly'] = True
			self.fields['id'].initial = initial['_id']
