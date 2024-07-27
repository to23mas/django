from django import forms

from domain.data.tests.enum.TargetUnlockType import TargetUnlockType


class TestEditForm(forms.Form):

	id = forms.IntegerField(required=False)
	title = forms.CharField()
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
	time = forms.IntegerField()
	target_type = forms.ChoiceField()
	target_id = forms.IntegerField(required=False)
	source_id = forms.IntegerField(required=False)
	attempts = forms.IntegerField()
	success_score = forms.IntegerField()
	total_points = forms.IntegerField(required=False)

	def __init__(self, *args, **kwargs):
		initial = kwargs.get('initial', {})
		super(TestEditForm, self).__init__(*args, **kwargs)
		self.fields['total_points'].widget.attrs['disabled'] = True
		self.fields['id'].widget.attrs['disabled'] = True
		self.fields['target_type'].choices = [(target.value, target.value) for target in TargetUnlockType]

		if initial:
			self.fields['id'].initial = initial['_id']
