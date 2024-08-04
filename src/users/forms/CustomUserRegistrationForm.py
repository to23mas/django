from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = (
			'username',
			'email',
			'password1',
			'password2'
		)
		help_texts = {
			# 'username': 'Custom help text for username.',
			# 'email': 'Custom help text for email.',
			# 'password1': 'Custom help text for password.',
			# 'password2': 'Custom help text for password confirmation.',
		}
		error_messages = {
			'username': {
				'required': 'Custom error: Username is required.',
				'unique': 'Custom error: This username is already taken.',
				'invalid': 'Custom error: Invalid username.',
			},
			'email': {
				'required': 'Custom error: Email is required.',
				'invalid': 'Custom error: Invalid email address.',
			},
			'password1': {
				'required': 'Custom error: Password is required.',
				'password_too_short': 'Custom error: Password is too short.',
				'password_too_common': 'Custom error: Password is too common.',
				'password_entirely_numeric': 'Custom error: Password cannot be entirely numeric.',
			},
			'password2': {
				'required': 'Custom error: Password confirmation is required.',
				'password_mismatch': 'Custom error: Passwords do not match.',
			}}

	def __init__(self, *args, **kwargs):
		super(CustomUserCreationForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Uživatelské jméno'
		self.fields['username'].help_text = ''

		self.fields['email'].label = 'Email'
		self.fields['email'].help_text = ''

		self.fields['password1'].label = 'Heslo'
		self.fields['password1'].help_text = ''

		self.fields['password2'].label = 'Heslo znovu'
		self.fields['password2'].help_text = ''
