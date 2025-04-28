from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
)
from django import forms
from django.core.exceptions import ValidationError
import re

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
        }
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
            'password2': {
                'required': 'Potvrzení hesla je povinné.',
                'password_mismatch': 'Hesla se neshodují.',
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Přenastavení popisů
        self.fields['username'].label = 'Uživatelské jméno'
        self.fields['email'].label = 'Email'
        self.fields['password1'].label = 'Heslo'
        self.fields['password2'].label = 'Heslo znovu'

        # Přenastavení help textů
        for field in self.fields:
            self.fields[field].help_text = ''

        # Přenastavení error_messages
        for field_name, messages in self.error_messages.items():
            if field_name in self.fields:
                self.fields[field_name].error_messages.update(messages)

        # Přidání vlastních validátorů s českými chybovými zprávami
        class CustomMinimumLengthValidator:
            def __init__(self, min_length=8):
                self.min_length = min_length

            def __call__(self, password, user=None):
                if len(password) < self.min_length:
                    raise ValidationError('Heslo je příliš krátké. Musí obsahovat alespoň 8 znaků.')

        class CustomCommonPasswordValidator:
            def __init__(self):
                self.passwords = set()

            def __call__(self, password, user=None):
                if password.lower().strip() in self.passwords:
                    raise ValidationError('Toto heslo je příliš běžné. Zvolte silnější heslo.')

        class CustomNumericPasswordValidator:
            def __call__(self, password, user=None):
                if password.isdigit():
                    raise ValidationError('Heslo nemůže být pouze číselné.')

        class CustomUserAttributeSimilarityValidator:
            def __init__(self):
                self.user_attributes = ('username', 'first_name', 'last_name', 'email')

            def __call__(self, password, user=None):
                if not user:
                    return
                for attribute_name in self.user_attributes:
                    value = getattr(user, attribute_name, None)
                    if not value or not isinstance(value, str):
                        continue
                    value_parts = re.findall(r'\w+', value.lower())
                    for value_part in value_parts:
                        if value_part in password.lower():
                            raise ValidationError('Heslo je příliš podobné emailové adrese.')

        class CustomPasswordMatchValidator:
            def __init__(self, form):
                self.form = form

            def __call__(self, password, user=None):
                if 'password1' in self.form.data and password != self.form.data['password1']:
                    raise ValidationError('Hesla se neshodují.')

        self.fields['password1'].validators = [
            CustomMinimumLengthValidator(min_length=8),
            CustomCommonPasswordValidator(),
            CustomNumericPasswordValidator(),
            CustomUserAttributeSimilarityValidator()
        ]

        # Přidání validátorů pro password2
        self.fields['password2'].validators = [
            CustomMinimumLengthValidator(min_length=8),
            CustomPasswordMatchValidator(self)
        ]

        # Přepsání chybových zpráv pro validaci hesla
        self.fields['password1'].error_messages = {
            'required': 'Heslo je povinné.',
            'password_too_short': 'Heslo je příliš krátké. Musí obsahovat alespoň 8 znaků.',
            'password_too_common': 'Toto heslo je příliš běžné. Zvolte silnější heslo.',
            'password_entirely_numeric': 'Heslo nemůže být pouze číselné.',
            'password_too_similar': 'Heslo je příliš podobné emailové adrese.',
        }

        # Přepsání chybových zpráv pro potvrzení hesla
        self.fields['password2'].error_messages = {
            'required': 'Potvrzení hesla je povinné.',
            'password_mismatch': 'Hesla se neshodují.',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password2']['password_mismatch'],
                code='password_mismatch',
            )
        return password2
