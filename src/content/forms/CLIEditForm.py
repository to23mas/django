from django import forms

class CLIEditForm(forms.Form):
	id = forms.IntegerField(required=False)
	title = forms.CharField()
	task_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 15}))
	expected_output = forms.CharField(widget=forms.Textarea(attrs={'rows': 15}))  # Expected output of the command

	def __init__(self, *args, **kwargs):
		initial = kwargs.get('initial', {})
		super(CLIEditForm, self).__init__(*args, **kwargs)
		if initial:
			self.fields['id'].initial = initial['_id']
		self.fields['id'].widget.attrs['disabled'] = True
