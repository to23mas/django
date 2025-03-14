from django.core.management.base import BaseCommand
# from app.birthdays.cron import test_mail
from birthdays.cron import test_mail
# from birthdays.utils import send_email_to_user

class Command(BaseCommand):
    help = 'Send birthday emails to users'

    def handle(self, *args, **kwargs):
        print('ahoj')
        test_mail()
