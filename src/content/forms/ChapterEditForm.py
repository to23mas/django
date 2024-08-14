from django import forms

from domain.data.chapters.enum.ChapterUnlockType import ChapterUnlockType
from domain.data.lessons.LessonStorage import find_lessons_by_course, get_lesson


class ChapterEditForm(forms.Form):

	id = forms.IntegerField(required=False)
	lesson_id = forms.ChoiceField(widget=forms.Select)
	title = forms.CharField()
	is_last = forms.BooleanField(required=False, initial=False)
	unlock_type = forms.ChoiceField(widget=forms.Select)
	unlock_id = forms.IntegerField()

	def __init__(self, *args, db=None, project_db=None, **kwargs):
		initial = kwargs.get('initial', {})
		super(ChapterEditForm, self).__init__(*args, **kwargs)

		if project_db and db:
			self.fields['lesson_id'].choices = [(project.id, project.title) for project in find_lessons_by_course(db, project_db)]
			if initial:
				self.fields['lesson_id'].initial = get_lesson(initial['lesson_id'], db, project_db)
		if initial:
			self.fields['id'].initial = initial['_id']

		self.fields['id'].widget.attrs['readonly'] = True
		self.fields['unlock_type'].choices = [(target.value, target.value) for target in ChapterUnlockType]

	def clean(self):
		cleaned_data = super().clean()

		lesson_value = cleaned_data.get('lesson_id')
		if lesson_value: cleaned_data['lesson_id'] = int(lesson_value)

		return cleaned_data
