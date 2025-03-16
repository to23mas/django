from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Book
from datetime import datetime
from django.core.management import call_command
from django.contrib import messages


@login_required
def index(request):
    return render(request, 'library/index.html')

@csrf_exempt
@login_required
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        return JsonResponse({'books': [book.to_dict() for book in books]})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            published_date = datetime.strptime(data.get('published_date'), '%Y-%m-%d').date() if data.get('published_date') else None
            
            book = Book.objects.create(
                title=data.get('title'),
                author=data.get('author'),
                isbn=data.get('isbn'),
                pages=data.get('pages'),
                published_date=published_date
            )
            return JsonResponse(book.to_dict(), status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': f'Invalid date format. Use YYYY-MM-DD. {str(e)}'}, status=400)

@csrf_exempt
@login_required
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse(book.to_dict())
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            book.title = data.get('title', book.title)
            book.author = data.get('author', book.author)
            if 'isbn' in data:
                book.isbn = data['isbn']
            if 'pages' in data:
                book.pages = data['pages']
            if 'published_date' in data:
                book.published_date = datetime.strptime(data['published_date'], '%Y-%m-%d').date()
            book.save()
            return JsonResponse(book.to_dict())
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': f'Invalid date format. Use YYYY-MM-DD. {str(e)}'}, status=400)
    
    elif request.method == 'DELETE':
        book.delete()
        return JsonResponse({}, status=204)

@login_required
def reset_data(request):
    try:
        # Clear existing data
        Book.objects.all().delete()
        
        # Load fixtures
        call_command('loaddata', 'library/fixtures/initial_books.json', verbosity=0)
        
        messages.success(request, 'Data reset successful!')
    except Exception as e:
        messages.error(request, f'Error resetting data: {str(e)}')
    
    return redirect('library_rest:index')
