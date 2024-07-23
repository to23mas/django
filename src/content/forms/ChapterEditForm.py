from django import forms

from domain.data.lessons.LessonStorage import find_lessons_by_course


class ChapterEditForm(forms.Form):

	no = forms.IntegerField()
	lesson = forms.ChoiceField(widget=forms.Select)
	title = forms.CharField()
	unlock_type = forms.CharField()
	unlock_no = forms.IntegerField()
	blocks = forms.CharField(
		widget=forms.Textarea(attrs={'rows': 15}),
	)

	def __init__(self, *args, db=None, **kwargs):
		super(ChapterEditForm, self).__init__(*args, **kwargs)

		if db:
			self.fields['lesson'].choices = [(int(project.no), project.title) for project in find_lessons_by_course(db)]

