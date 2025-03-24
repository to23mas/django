from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from typing import Dict
from django.urls import reverse
from django.shortcuts import redirect

# In-memory storage
BOOKS: Dict[int, dict] = {
	1: {
		"id": 1,
		"title": "The Hobbit",
		"author": "J.R.R. Tolkien",
		"isbn": "978-0547928227",
		"pages": 300,
		"published_date": "1937-09-21"
	},
	2: {
		"id": 2,
		"title": "1984",
		"author": "George Orwell",
		"isbn": "978-0451524935",
		"pages": 328,
		"published_date": "1949-06-08"
	}
}
NEXT_ID = 3

@csrf_exempt
def api_books(request: HttpRequest, course: str, demo_id: int) -> JsonResponse:

	global NEXT_ID

	if request.method == 'GET':
		return JsonResponse({'books': list(BOOKS.values())})

	elif request.method == 'POST':
		try:
			data = json.loads(request.body)
			new_book = {
				'id': NEXT_ID,
				'title': data['title'],
				'author': data['author'],
				'isbn': data['isbn'],
				'pages': data['pages'],
				'published_date': data['published_date']
			}
			BOOKS[NEXT_ID] = new_book
			NEXT_ID += 1
			return JsonResponse(new_book, status=201)
		except (json.JSONDecodeError, KeyError):
			return JsonResponse({'error': 'Invalid data'}, status=400)

@csrf_exempt
def api_book_detail(request: HttpRequest, course: str, demo_id: int, book_id: int) -> JsonResponse:
	if book_id not in BOOKS:
		return JsonResponse({'error': 'Book not found'}, status=404)

	if request.method == 'GET':
		return JsonResponse(BOOKS[book_id])

	elif request.method == 'PUT':
		try:
			data = json.loads(request.body)
			BOOKS[book_id].update({
				'title': data.get('title', BOOKS[book_id]['title']),
				'author': data.get('author', BOOKS[book_id]['author']),
				'isbn': data.get('isbn', BOOKS[book_id]['isbn']),
				'pages': data.get('pages', BOOKS[book_id]['pages']),
				'published_date': data.get('published_date', BOOKS[book_id]['published_date'])
			})
			return JsonResponse(BOOKS[book_id])
		except (json.JSONDecodeError, KeyError):
			return JsonResponse({'error': 'Invalid data'}, status=400)

	elif request.method == 'DELETE':
		book = BOOKS.pop(book_id)
		return JsonResponse(book)

def reset_data_rest(request: HttpRequest, course: str, demo_id: int):
	global BOOKS, NEXT_ID
	BOOKS.clear()
	NEXT_ID = 3
	BOOKS.update({
		1: {
			"id": 1,
			"title": "The Hobbit",
			"author": "J.R.R. Tolkien",
			"isbn": "978-0547928227",
			"pages": 300,
			"published_date": "1937-09-21"
		},
		2: {
			"id": 2,
			"title": "1984",
			"author": "George Orwell",
			"isbn": "978-0451524935",
			"pages": 328,
			"published_date": "1949-06-08"
		}
	})
	return redirect(reverse('demos:library_rest', args=[course, demo_id]))
