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
		help_texts = {}
		error_messages = {
			'username': {
				'required': 'Uživatelské jméno je povinné.',
				'unique': 'Toto uživatelské jméno je již obsazené.',
				'invalid': 'Neplatné uživatelské jméno.',
			},
			'email': {
				'required': 'Email je povinný.',
				'invalid': 'Neplatná emailová adresa.',
			},
			'password1': {
				'required': 'Heslo je povinné.',
				'password_too_short': 'Heslo je příliš krátké.',
				'password_too_common': 'Heslo je příliš běžné.',
				'password_entirely_numeric': 'Heslo nemůže být pouze číselné.',
				'password_too_similar': 'Heslo je příliš podobné emailové adrese.',
			},
			'password2': {
				'required': 'Potvrzení hesla je povinné.',
				'password_mismatch': 'Hesla se neshodují.',
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
