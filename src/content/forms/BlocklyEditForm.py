from django import forms


class BlocklyEditForm(forms.Form):

	id = forms.IntegerField(required=False)
	title = forms.CharField()
	task_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 15}))
	expected_task = forms.CharField()
	expected_result = forms.CharField()
	title = forms.CharField()
	toolbox = forms.CharField(widget=forms.Textarea(attrs={'rows': 15}))

	def __init__(self, *args, **kwargs):
		initial = kwargs.get('initial', {})
		super(BlocklyEditForm, self).__init__(*args, **kwargs)
		if initial:
			self.fields['id'].initial = initial['_id']
		self.fields['id'].widget.attrs['disabled'] = True
