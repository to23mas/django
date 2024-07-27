from django import forms

from domain.data.chapters.enum.ChapterUnlockType import ChapterUnlockType
from domain.data.lessons.LessonStorage import find_lessons


class ChapterFilterForm(forms.Form):

	title = forms.CharField(required=False)
	lesson_id = forms.ChoiceField(required=False, widget=forms.Select)
	unlock_type = forms.ChoiceField(required=False, widget=forms.Select)
	unlock_id = forms.IntegerField(required=False)

	def __init__(self, *args, db=None, project_db=None, **kwargs):
		super(ChapterFilterForm, self).__init__(*args, **kwargs)
		if db and project_db:
			lessons = find_lessons(db, project_db)
			if lessons:
				self.fields['lesson_id'].choices = [('', 'All')] + [(int(lesson.id), lesson.title) for lesson in lessons]

		self.fields['unlock_type'].choices = [('', 'All')] + [(target.value, target.value) for target in ChapterUnlockType]

	def clean(self):
		cleaned_data = super().clean()
		cleaned_data = {key: value for key, value in cleaned_data.items() if value not in [None, '']}

		lesson_value = cleaned_data.get('lesson_id')
		if lesson_value: cleaned_data['lesson_id'] = int(lesson_value)

		return cleaned_data
