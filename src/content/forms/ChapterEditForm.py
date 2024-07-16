from django import forms


class ChapterEditForm(forms.Form):

	no = forms.IntegerField()
	lesson = forms.IntegerField()
	project = forms.IntegerField()
	title = forms.CharField()
	unlock_type = forms.CharField()
	unlock_no = forms.IntegerField()
