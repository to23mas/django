"""Login module

- contains logins sreen
- functionalities: registration. login. logout
"""
from django.apps import AppConfig


class LoginConfig(AppConfig):
    """login screen"""
    default_auto_field = "django.db.models.BigAutoField"
    name = "login"
