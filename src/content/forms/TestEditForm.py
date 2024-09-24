from django import forms


class TestEditForm(forms.Form):

	id = forms.IntegerField(required=False)
	title = forms.CharField()
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
	time = forms.IntegerField()
	unlock_lesson = forms.IntegerField(required=False)
	unlock_chapter = forms.IntegerField(required=False)
	unlock_project = forms.IntegerField(required=False)
	finish_project = forms.IntegerField(required=False)
	finish_lesson = forms.IntegerField(required=False)
	finish_chapter = forms.IntegerField(required=False)
	attempts = forms.IntegerField()
	success_score = forms.IntegerField()
	total_points = forms.IntegerField(required=False)

	def __init__(self, *args, **kwargs):
		initial = kwargs.get('initial', {})
		super(TestEditForm, self).__init__(*args, **kwargs)
		self.fields['total_points'].widget.attrs['disabled'] = True
		self.fields['id'].widget.attrs['disabled'] = True

		if initial:
			self.fields['id'].initial = initial['_id']
