from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from jsonrpcserver import method, Success, dispatch
import json

# Use the same initial books data
INITIAL_BOOKS = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "9780743273565", "pages": 180, "published_date": "1925-04-10"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "isbn": "9780446310789", "pages": 281, "published_date": "1960-07-11"},
    {"id": 3, "title": "1984", "author": "George Orwell", "isbn": "9780451524935", "pages": 328, "published_date": "1949-06-08"},
]

books = list(INITIAL_BOOKS)

@method
def get_books():
    global books  # Make sure we're using the global list
    return Success(books)

@method
def get_book(id: int):
    global books  # Make sure we're using the global list
    book = next((b for b in books if b['id'] == id), None)
    if book is None:
        raise Exception("Book not found")
    return Success(book)

@method
def create_book(title: str, author: str, isbn: str, pages: int, published_date: str):
    global books  # Make sure we're using the global list
    new_id = max(book['id'] for book in books) + 1
    new_book = {
        'id': new_id,
        'title': title,
        'author': author,
        'isbn': isbn,
        'pages': pages,
        'published_date': published_date
    }
    books.append(new_book)
    return Success(new_book)

@method
def update_book(id: int, title: str = None, author: str = None, 
                isbn: str = None, pages: int = None, published_date: str = None):
    global books  # Make sure we're using the global list
    book = next((b for b in books if b['id'] == id), None)
    if book is None:
        raise Exception("Book not found")
    
    if title is not None: book['title'] = title
    if author is not None: book['author'] = author
    if isbn is not None: book['isbn'] = isbn
    if pages is not None: book['pages'] = pages
    if published_date is not None: book['published_date'] = published_date
    
    return Success(book)

@method
def delete_book(id: int):
    global books
    initial_length = len(books)
    books = [b for b in books if b['id'] != id]
    return Success({"success": len(books) < initial_length})

def library_jsonrpc(request, course, demo_id):
    context = {
        'course': course,
        'demo': {'id': demo_id},
    }
    return render(request, 'demos/demo/library_jsonrpc.html', context)

@csrf_exempt
def jsonrpc_endpoint(request, course, demo_id):
    if request.method != 'POST':
        return JsonResponse({"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": None})
    
    try:
        request_data = request.body.decode('utf-8')
        response = dispatch(request_data)
        return JsonResponse(json.loads(str(response)))
    except Exception as e:
        return JsonResponse({
            "jsonrpc": "2.0",
            "error": {"code": -32700, "message": str(e)},
            "id": None
        })

def reset_data_jsonrpc(request, course, demo_id):
    global books
    books.clear()
    books.extend(INITIAL_BOOKS)
    return redirect('demos:library_jsonrpc', course=course, demo_id=demo_id) 