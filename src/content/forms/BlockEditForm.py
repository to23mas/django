from django import forms


class SummernoteWidget(forms.Textarea):
	def __init__(self, *args, **kwargs):
		kwargs['attrs'] = {'id': 'summernote', 'name': 'editordata'}
		super().__init__(*args, **kwargs)

class BlockEditForm(forms.Form):

	id = forms.IntegerField(required=False)
	title = forms.CharField()
	order = forms.IntegerField()

	text = forms.CharField(
		required=False,
		widget=forms.Textarea(attrs={
			'id': 'summernote',
			'name': 'editordata'
	}))
	def __init__(self, *args, **kwargs):
		super(BlockEditForm, self).__init__(*args, **kwargs)
		self.fields['id'].widget.attrs['readonly'] = True
