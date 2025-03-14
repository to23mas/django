from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from .models import Birthday
from .forms import BirthdayForm
from .cron import check_nameday, test_mail

def birthday_list(request):
    if request.method == 'POST':
        form = BirthdayForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Birthday added successfully!')
            return redirect('birthdays:birthday_list')
    else:
        form = BirthdayForm()

    birthdays = Birthday.objects.all()

    # Get cron status for staff members
    cron_jobs = None
    if request.user.is_staff:
        try:
            cron_jobs = call_command('crontab', 'show', stdout=True)
        except Exception:
            cron_jobs = "No cron jobs configured"

    return render(request, 'birthdays/birthday_list.html', {
        'form': form,
        'birthdays': birthdays,
        'cron_jobs': cron_jobs
    })

def delete_birthday(request, birthday_id):
    birthday = get_object_or_404(Birthday, pk=birthday_id)
    if request.method == 'POST':
        birthday.delete()
        messages.success(request, f'Birthday for {birthday.name} was deleted successfully!')
    return redirect('birthdays:birthday_list')

@staff_member_required
def test_birthday_email(request):
    """Test view to manually trigger birthday emails."""
    test_mail()
    # check_nameday()
    messages.success(request, "Birthday notification emails have been sent!")
    return redirect('birthdays:birthday_list')

@staff_member_required
def manage_cron(request, action):
    """Manage cron jobs."""
    try:
        if action == 'add':
            call_command('crontab', 'add')
            messages.success(request, 'Cron jobs added successfully!')
        elif action == 'remove':
            call_command('crontab', 'remove')
            messages.success(request, 'Cron jobs removed successfully!')
        elif action == 'show':
            output = call_command('crontab', 'show')
            messages.info(request, f'Current cron jobs: {output}')
    except Exception as e:
        messages.error(request, f'Error managing cron jobs: {str(e)}')

    return redirect('birthdays:birthday_list')
