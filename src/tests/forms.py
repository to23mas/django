from typing import List
from django import forms

from domain.data.tests.QuestionData import QuestionData

class DynamicTestForm(forms.Form):
    def __init__(self, questionDataCollection: List[QuestionData], *args, **kwargs):
        super().__init__(*args, **kwargs)

        for question in questionDataCollection:

            if question.type == 'single':
                self.fields[question.question] = forms.ChoiceField(
                    label=question.question,
                    choices=question.answers,
                    widget=forms.RadioSelect())

            elif question.type == 'multiple':
                self.fields[question.question] = forms.MultipleChoiceField(
                    label=question.question.capitalize(),
                    choices=question.answers,
                    widget=forms.CheckboxSelectMultiple())

            elif question.type == 'open':
                self.fields[question.question] = forms.CharField(
                    label=question.question.capitalize(),
                    max_length=250,
                    widget=forms.TextInput())
