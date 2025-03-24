from django import forms


class DemoEditForm(forms.Form):

	id = forms.IntegerField(required=False)
	project_id = forms.IntegerField(required=False)
	name = forms.CharField()
	url = forms.CharField()

	def __init__(self, *args, **kwargs):
		initial = kwargs.get('initial', {})
		super(DemoEditForm, self).__init__(*args, **kwargs)
		if initial:
			self.fields['id'].initial = initial['_id']
		self.fields['id'].widget.attrs['disabled'] = True
