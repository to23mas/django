from django import forms


class TestEditForm(forms.Form):

	no = forms.IntegerField()
	title = forms.CharField()
	description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
	time = forms.IntegerField()
	target_type = forms.CharField()
	target_no = forms.IntegerField()
	source_no = forms.IntegerField()
	attempts = forms.IntegerField()
	success_score = forms.IntegerField()
	total_points = forms.IntegerField()

	def __init__(self, *args, **kwargs):
		super(TestEditForm, self).__init__(*args, **kwargs)
		self.fields['total_points'].widget.attrs['disabled'] = True
