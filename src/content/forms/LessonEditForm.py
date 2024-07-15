from django import forms


class LessonEditForm(forms.Form):

	id = forms.CharField()
	no = forms.IntegerField()
	project= forms.IntegerField()
	title = forms.CharField()

	def __init__(self, *args, **kwargs):
		super(LessonEditForm, self).__init__(*args, **kwargs)
		self.fields['id'].widget.attrs['disabled'] = True
