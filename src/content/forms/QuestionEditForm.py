from django import forms
import ast

from domain.data.tests.enum.QuestionType import QuestionType


class QuestionEditForm(forms.Form):

	id = forms.IntegerField(required=False)
	question = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
	type = forms.ChoiceField(widget=forms.Select)
	points = forms.IntegerField()
	correct = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
	answers = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5}))

	def __init__(self, *args, **kwargs):
		initial = kwargs.get('initial', {})
		kwargs['initial'] = initial
		if 'correct' in initial and isinstance(initial['correct'], list):
			initial['correct'] = ', '.join(initial['correct'])

		super(QuestionEditForm, self).__init__(*args, **kwargs)

		if initial:
			self.fields['id'].initial = initial['_id']
		self.fields['id'].widget.attrs['disabled'] = True
		self.fields['type'].choices = [(target.value, target.value) for target in QuestionType]


	def clean_answers(self):
		data = self.cleaned_data['answers']
		if (data == None or data == ''):
			return {}
		return ast.literal_eval(data)

	def clean_correct(self):
		data = self.cleaned_data['correct']

		if isinstance(data, str):
			string_list = [s.strip() for s in data.split(',') if s.strip()]
		else:
			string_list = [str(data).strip()]

		return string_list
