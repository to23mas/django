from datetime import date, datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import request
from .models import Birthday
import requests

def test_cron_job():
    """Test cron job that runs every minute."""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("--------------------------------")
    print(f"[{current_time}] Test cron job is running!")
    print("--------------------------------")

def send_birthday_emails():
    """Send birthday notification emails to admin."""
    today = date.today()
    birthdays = Birthday.objects.filter(
        birth_date__month=today.month,
        birth_date__day=today.day
    )
    
    if birthdays.exists():
        # Get admin email
        User = get_user_model()
        admin_email = User.objects.get(username='admin').email
        
        # Create email content
        subject = f"Birthday Notifications for {today.strftime('%B %d')}"
        message = "Today's Birthdays:\n\n"
        
        for birthday in birthdays:
            message += f"🎉 {birthday.name}\n"
        
        message += "\nBest wishes,\nBirthday Tracker"
        
        # Send email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            fail_silently=False,
        )

def test_mail():
    print('sending test mail')
    User = get_user_model()
    admin_email = User.objects.get(username='admin').email
    subject = "Test Email from Birthday App"
    message = "This is a test email. If you received this, the email configuration is working correctly."

    return send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[admin_email],
        fail_silently=False,
    ) 

def check_nameday():
    """Check and send notification about today's name day."""
    try:
        response = requests.get('https://svatkyapi.cz/api/day')
        if response.status_code == 200:
            data = response.json()
            nameday_name = data['name']
            date = data['date']
            
            matching_birthdays = Birthday.objects.filter(calendar_name=nameday_name)
            
            if matching_birthdays.exists():
                User = get_user_model()
                admin_email = User.objects.get(username='admin').email
                
                subject = f"Name Day Notification for {date}"
                message = f"Today ({date}) is the name day of {nameday_name}!\n\n"
                for birthday in matching_birthdays:
                    message += f"🎉 {birthday.name} (born {birthday.birth_date.strftime('%d/%m/%Y')})\n"
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[admin_email],
                    fail_silently=False,
                )
    except Exception as e:
        print(f"Error checking name day: {str(e)}")
