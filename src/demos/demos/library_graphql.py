from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from django.contrib import messages
from .schema import books
from domain.data.demos.DemoStorage import DemoStorage
from domain.data.progress.ProgressStorage import ProgressStorage

def _check(request: HttpRequest, course: str, demo_id: int):
	username = request.user.username #type: ignore
	if (ProgressStorage().get_user_progress_by_course(username, course) is None):
		messages.warning(request, 'Kurz ještě není odemčen!')
		return redirect('courses:overview')

	demo = DemoStorage().get_demo(demo_id, course)
	if demo is None:
		messages.warning(request, 'Ukázkový projekt není v tyto chvíli dostupný')
		return redirect('courses:overview')

	project_url = reverse('projects:detail', kwargs={'course': course, 'project_id': demo_id})
	return username, demo, course, project_url

def library_graphql(request, course, demo_id):
	context = {
		'course': course,
		'demo': {'id': demo_id},
	}
	return render(request, 'demos/demo/library_graphql.html', context)

def reset_data_graph(request: HttpRequest, course: str, demo_id: int):
	result = _check(request, course, demo_id)
	if not isinstance(result, tuple):  # If _check returned a redirect
		return result

	username, demo, course, project_url = result

	global books
	books = [
		{"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "9780743273565", "pages": 180, "published_date": "1925-04-10"},
		{"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "isbn": "9780446310789", "pages": 281, "published_date": "1960-07-11"},
		{"id": 3, "title": "1984", "author": "George Orwell", "isbn": "9780451524935", "pages": 328, "published_date": "1949-06-08"},
	]

	return redirect('demos:library_graphql', course=course, demo_id=demo_id)
