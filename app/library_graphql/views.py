from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.management import call_command
from library_rest.models import Book  
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'library_graphql/index.html')

def reset_data(request):
    try:
        # Clear existing data
        Book.objects.all().delete()
        
        # Load fixtures
        call_command('loaddata', 'library_rest/fixtures/initial_books.json', verbosity=0)
        
        messages.success(request, 'Data reset successful!')
    except Exception as e:
        messages.error(request, f'Error resetting data: {str(e)}')
    
    return redirect('library_graphql:index')
