# Birthday Tracker App

A Django application that helps track birthdays and sends automated email notifications.

## Features

- Add birthdays with name, date, and email
- View all birthdays in a list format
- Automatic email notifications on people's birthdays
- Admin interface for managing birthdays
- Modern UI using Tailwind CSS

## Setup Instructions

1. Install required packages:
   ```bash
   pip install django-crontab==0.7.1
   ```

2. Run database migrations:
   ```bash
   python manage.py makemigrations birthdays
   python manage.py migrate
   ```

3. Configure email settings in your environment variables:
   ```bash
   # Add these to your .env file
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```
   Note: If using Gmail, you'll need to:
   - Enable 2-Factor Authentication
   - Generate an App Password (Google Account → Security → App Passwords)
   - Use the generated App Password as EMAIL_HOST_PASSWORD

4. Set up the crontab for email notifications:
   ```bash
   python manage.py crontab add
   ```

5. Verify crontab installation:
   ```bash
   python manage.py crontab show
   ```

6. Monitor cron jobs in Docker:
   ```bash
   # Check if cron is running
   docker compose exec web service cron status
   
   # Monitor cron logs in real-time
   docker compose exec web tail -f /var/log/cron.log
   ```

## Project Structure

```
app/birthdays/
├── migrations/
├── templates/
│   └── birthdays/
│       └── birthday_list.html
├── __init__.py
├── admin.py
├── apps.py
├── cron.py
├── forms.py
├── models.py
├── urls.py
└── views.py
```

## Models

### Birthday Model
- `name`: CharField - Person's name
- `birth_date`: DateField - Date of birth
- `email`: EmailField - Email for notifications
- `created_at`: DateTimeField - Record creation timestamp

## Views

### birthday_list
- URL: `/birthdays/`
- Displays form to add new birthdays
- Shows list of all birthdays
- Handles form submission for new birthdays

## Cron Jobs

The application uses django-crontab to send birthday emails automatically:
- Runs daily at midnight (0 0 * * *)
- Checks for birthdays on the current day
- Sends personalized email notifications

## Email Configuration

The app uses Gmail SMTP for sending emails. To set up:

1. Go to your Google Account settings (https://myaccount.google.com/)
2. Enable 2-Step Verification if not already enabled
3. Go to Security → App passwords (or visit https://myaccount.google.com/apppasswords)
4. Generate new App Password:
   - Select "Mail" and "Other (Custom name)"
   - Name it "Django Birthday App"
   - Copy the 16-character password generated

5. Set environment variables:
```bash
# Add to your ~/.bashrc or ~/.zshrc
export EMAIL_HOST_USER="your-email@gmail.com"
export EMAIL_HOST_PASSWORD="your-16-char-app-password"
```

Default email settings in settings.py:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

## Testing Email Functionality

1. Log in as a staff user
2. Go to the birthday list page
3. Click the "Test Email" button to send a test notification
4. Check your admin email for the test message

## Troubleshooting

### Email Issues
1. Verify your environment variables are set correctly:
```bash
echo $EMAIL_HOST_USER
echo $EMAIL_HOST_PASSWORD
```

2. Make sure you're using an App Password, not your regular Gmail password

3. Common error messages:
   - "SMTPAuthenticationError": Check your credentials
   - "SMTPServerDisconnected": Check your internet connection
   - "ConnectionRefusedError": Verify SMTP settings and port

### Cron Job Issues
1. Check if crontab is installed:
```bash
python manage.py crontab show
```

2. Install/update crontab jobs:
```bash
docker compose exec web python manage.py crontab add
```

3. View cron logs in Docker:
```bash
docker compose exec web tail -f /var/log/cron.log
```

4. Remove crontab if needed:
```bash
docker compose exec web python manage.py crontab remove
```

### Database Issues
1. Reset migrations if needed:
```bash
python manage.py migrate birthdays zero
python manage.py migrate birthdays
```

2. Check for database integrity:
```bash
python manage.py dbshell
SELECT * FROM birthdays_birthday;
```

## Security Notes

1. Never commit email credentials to version control
2. Always use environment variables for sensitive data
3. Regularly rotate your App Password
4. Keep Django and all dependencies updated

## Future Enhancements

1. Multiple email templates
2. Customizable notification times
3. Birthday categories/tags
4. Export/import functionality
5. Calendar integration

## Usage

1. Access the birthday tracker at `/birthdays/`
2. Add new birthdays using the form
3. View all birthdays in the list below the form
4. Emails will be automatically sent at midnight on each person's birthday

## Admin Interface

Access the admin interface at `/admin/` to:
- View all birthdays
- Add/Edit/Delete birthday records
- Filter birthdays by date
- Search by name or email

## Troubleshooting

1. If emails are not sending:
   - Verify email credentials in environment variables
   - Check if crontab is properly installed
   - Ensure SMTP settings match your email provider

2. To check crontab logs:
   ```bash
   grep CRON /var/log/syslog
   ```

3. To remove crontab:
   ```bash
   python manage.py crontab remove
   ```
