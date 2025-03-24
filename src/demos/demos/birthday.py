from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.urls import reverse
from domain.data.demos.DemoStorage import DemoStorage
from domain.data.progress.ProgressStorage import ProgressStorage
from django.http import HttpRequest

# Define the BirthdayForm within this file

# Temporary storage for birthdays (in-memory)
birthdays = []

def _check(request: HttpRequest, course: str, demo_id: int):
	username = request.user.username #type: ignore
	if (ProgressStorage().get_user_progress_by_course(username, course) is None):
		messages.warning(request, 'Kurz ještě není odemčen!')
		return redirect('courses:overview')

	demo = DemoStorage().get_demo(demo_id, course)
	if demo is None:
		messages.warning(request, 'Ukázkový projekt není v tyto chvíli dostupný')
		return redirect('courses:overview')

	# TODO uncomment when project is ready
	# user_available = ProgressStorage().find_available_demos(course, username)
	# if user_available is None or demo.id not in user_available:
	# 	messages.warning(request, 'Ukázkový projekt ještě není odemčen')
	# 	return redirect('courses:overview', course=course)

	# project = ProjectStorage().get_project_by_id(demo_id, course)
	# if project is None:
	# 	messages.error(request, 'nevalidní akce')
	# 	return redirect('courses:overview', course=course)

	# project_url = reverse('projects:detail', kwargs={'course': course, 'project_id': project.id})
	project_url = reverse('projects:detail', kwargs={'course': course, 'project_id': 1})

	return username, demo, course, project_url


def birthday(request: HttpRequest, course: str, demo_id: int):
	username, demo, course, project_url = _check(request, course, demo_id)
	if request.method == 'POST':
		form = BirthdayForm(request.POST)
		if form.is_valid():
			birthday_entry = {
				'id': len(birthdays),  # Simple ID generation
				**form.cleaned_data
			}
			birthdays.append(birthday_entry)
			return redirect('demos:birthday', course=course, demo_id=demo_id)
	else:
		form = BirthdayForm()
	return render(request, 'demos/demo/birthday.html', {
		'form': form,
		'birthdays': birthdays,
		'username': username,
		'course': course,
		'project_url': project_url,
		'demo': demo,
	})

def delete_birthday(request: HttpRequest, course: str, demo_id: int, pk):
	username, demo, course, project_url = _check(request, course, demo_id)
	if 0 <= pk < len(birthdays):
		del birthdays[pk]  # Remove the birthday from the list
	return redirect('demos:birthday', course=course, demo_id=demo_id)

class BirthdayForm(forms.Form):
	name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500',
			'placeholder': 'Enter name'
		}),
		label='Name',
	)
	birth_date = forms.DateField(
		widget=forms.DateInput(attrs={
			'type': 'date',
			'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500'
		}),
		label='Birth Date',
	)
	calendar_name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={
			'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500',
			'placeholder': 'Enter calendar name'
		}),
		label='Calendar Name',
	)

	def clean(self):
		cleaned_data = super().clean()
		name = cleaned_data.get('name')
		birth_date = cleaned_data.get('birth_date')

		# Example validation: Check if the name is not empty
		if name and not name.strip():
			raise ValidationError('Name cannot be empty.')
		return cleaned_data
