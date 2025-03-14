# Birthday Tracker

A Django application to track birthdays and send email notifications.

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run migrations:
```bash
python manage.py migrate
```
4. Create a superuser:
```bash
python manage.py createsuperuser
```

## Email Configuration

To enable email notifications, you need to set up Gmail SMTP:

1. Go to your Google Account settings (https://myaccount.google.com/)
2. Enable 2-Step Verification if not already enabled
3. Go to Security → App passwords (or visit https://myaccount.google.com/apppasswords)
4. Generate new App Password:
   - Select "Mail" and "Other (Custom name)"
   - Name it "Django Birthday App"
   - Copy the 16-character password generated

5. Set environment variables:
```bash
export EMAIL_HOST_USER="your-email@gmail.com"
export EMAIL_HOST_PASSWORD="your-16-char-app-password"
```

You can add these to your `~/.bashrc` or `~/.zshrc` for persistence.

## Cron Jobs

The application uses cron jobs to send birthday notifications. To monitor the cron jobs:

1. Check if cron is running:
```bash
docker compose exec web service cron status
```

2. Monitor the cron log:
```bash
docker compose exec web tail -f /var/log/cron.log
```

## Features

- Add and manage birthdays
- Automatic email notifications for upcoming birthdays
- Manual test email functionality for admins
- Responsive UI with Tailwind CSS

## Running the Application

```bash
python manage.py runserver
```

Visit http://localhost:8000 to access the application. 