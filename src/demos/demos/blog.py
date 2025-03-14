from django import forms
from django.shortcuts import redirect, render, reverse
from django.contrib import messages
from django.http import HttpRequest
from domain.data.demos.DemoStorage import DemoStorage
from domain.data.progress.ProgressStorage import ProgressStorage
from domain.data.projects.ProjectStorage import ProjectStorage

from django.shortcuts import render, redirect


# Helper functions to interact with session
def _check(request: HttpRequest, course: str, demo_id: int):
	username = request.user.username #type: ignore
	if (ProgressStorage().get_user_progress_by_course(username, course) is None):
		messages.warning(request, 'Kurz ještě není odemčen!')
		return redirect('courses:overview')

	demo = DemoStorage().get_demo(demo_id, course)
	if demo is None:
		messages.warning(request, 'Ukázkový projekt není v tyto chvíli dostupný')
		return redirect('courses:overview')

	# TODO uncomment when project is ready
	# user_available = ProgressStorage().find_available_demos(course, username)
	# if user_available is None or demo.id not in user_available:
	# 	messages.warning(request, 'Ukázkový projekt ještě není odemčen')
	# 	return redirect('courses:overview', course=course)

	# project = ProjectStorage().get_project_by_id(demo_id, course)
	# if project is None:
	# 	messages.error(request, 'nevalidní akce')
	# 	return redirect('courses:overview', course=course)

	# project_url = reverse('projects:detail', kwargs={'course': course, 'project_id': project.id})
	project_url = reverse('projects:detail', kwargs={'course': course, 'project_id': 1})

	return username, demo, course, project_url

def get_posts_from_session(request):
	return request.session.get('posts', [])

def save_posts_to_session(request, posts):
	request.session['posts'] = posts

def get_categories_from_session(request):
	return request.session.get('categories', [])

def save_categories_to_session(request, categories):
	request.session['categories'] = categories

# ----------- Post Views -------------

def blog_1(request: HttpRequest, course: str, demo_id: int):
	username, demo, course, project_url = _check(request, course, demo_id)
	posts = get_posts_from_session(request)
	categories = get_categories_from_session(request)
	category_filter = request.GET.get('category')

	if category_filter:
		posts = [post for post in posts if str(category_filter) in post['categories']]

	return render(request, 'demos/demo/blog_post_list.html', {
		'posts': posts,
		'categories': categories,
		'username': username,
		'course': course,
		'project_url': project_url,
		'demo': demo,
	})

def post_detail(request: HttpRequest, course: str, demo_id: int, pk):
	username, demo, course, project_url = _check(request, course, demo_id)
	posts = get_posts_from_session(request)
	post = next((post for post in posts if post['id'] == pk), None)
	categories = get_categories_from_session(request)
	post_categories = post['categories']
	filtered_names = [c['name'] for c in categories if str(c['id']) in post_categories]

	return render(request, 'demos/demo/blog_post_detail.html', {
		'post': post,
		'username': username,
		'course': course,
		'project_url': project_url,
		'demo': demo,
		'categories': filtered_names,
	})

def post_create(request: HttpRequest, course: str, demo_id: int):
	username, demo, course, project_url = _check(request, course, demo_id)
	if request.method == 'POST':
		form = PostForm(request.POST, request=request)
		if form.is_valid():
			new_post_id = form.save_to_session(request)

			return redirect('demos:post_edit', course=course, demo_id=demo_id, pk=new_post_id)
	else:
		form = PostForm(request=request)

	return render(request, 'demos/demo/blog_post_form.html', {
		'form': form,
		'username': username,
		'course': course,
		'project_url': project_url,
		'demo': demo,
	})

def post_edit(request: HttpRequest, course: str, demo_id: int, pk):
	username, demo, course, project_url = _check(request, course, demo_id)
	posts = get_posts_from_session(request)
	post = next((post for post in posts if post['id'] == pk), None)

	if request.method == 'POST':
		form = PostForm(request.POST, request=request)
		if form.is_valid():
			new_post_id = form.save_to_session(request, post['id'])
			return redirect('demos:post_edit',course=course, demo_id=demo_id, pk=new_post_id)
	else:
		form = PostForm(initial={'title': post['title'], 'content': post['content']}, selected_categories=post['categories'], request=request)

	return render(request, 'demos/demo/blog_post_form.html', {
		'form': form,
		'post': post,
		'username': username,
		'course': course,
		'project_url': project_url,
		'demo': demo,
	})

def post_delete(request: HttpRequest, course: str, demo_id: int, pk):
	username, demo, course, project_url = _check(request, course, demo_id)
	posts = get_posts_from_session(request)
	posts = [post for post in posts if post['id'] != pk]
	save_posts_to_session(request, posts)

	return redirect('demos:blog_1', course=course, demo_id=demo_id)

# ----------- Category Views -------------

def category_list(request: HttpRequest, course: str, demo_id: int):
	username, demo, course, project_url = _check(request, course, demo_id)
	categories = get_categories_from_session(request)

	return render(request, 'demos/demo/blog_category_list.html', {
		'categories': categories,
		'username': username,
		'course': course,
		'project_url': project_url,
		'demo': demo,
	})

def category_detail(request: HttpRequest, course: str, demo_id: int, pk):
	username, demo, course, project_url = _check(request, course, demo_id)
	categories = get_categories_from_session(request)
	category = next((cat for cat in categories if cat['id'] == pk), None)

	return render(request, 'demos/demo/blog_category_detail.html', {
		'category': category,
		'username': username,
		'course': course,
		'project_url': project_url,
		'demo': demo,
	})

def category_create(request: HttpRequest, course: str, demo_id: int):
	username, demo, course, project_url = _check(request, course, demo_id)
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			new_category_id = form.save_to_session(request)
			return redirect('demos:category_edit', course=course, demo_id=demo_id, id=new_category_id)
	else:
		form = CategoryForm()

	return render(request, 'demos/demo/blog_category_form.html', {
		'form': form,
		'username': username,
		'course': course,
		'project_url': project_url,
		'demo': demo,
	})

def category_edit(request: HttpRequest, course: str, demo_id: int, id):
	username, demo, course, project_url = _check(request, course, demo_id)

	categories = request.session.get('categories', [])
	category = next((cat for cat in categories if cat['id'] == id), None)

	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			new_category_id = form.save_to_session(request, category_id=id)
			return redirect('demos:category_edit', course=course, demo_id=demo_id, id=new_category_id)
	else:
		form = CategoryForm(initial={'name': category['name']})

	return render(request, 'demos/demo/blog_category_form.html', {
		'form': form,
		'category': category,
		'username': username,
		'course': course,
		'project_url': project_url,
		'demo': demo,
	})

def category_delete(request: HttpRequest, course: str, demo_id: int, id):
	username, demo, course, project_url = _check(request, course, demo_id)
	categories = request.session.get('categories', [])
	categories = [cat for cat in categories if cat['id'] != id]
	request.session['categories'] = categories

	return redirect('demos:category_list', course=course, demo_id=demo_id)


class PostForm(forms.Form):
	title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
		'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500',
		'placeholder': 'Zadejte název příspěvku'
	}))

	content = forms.CharField(widget=forms.Textarea(attrs={
		'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500',
		'rows': 5,
		'placeholder': 'Napište obsah příspěvku...'
	}))

	categories = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
		'class': 'space-y-2 m-4'
	}), required=False)

	def __init__(self, *args, selected_categories=None, **kwargs):
		"""Load categories dynamically from the session and preselect them."""
		self.request = kwargs.pop('request', None)  # Extract request if provided
		super().__init__(*args, **kwargs)

		if self.request:
			categories = self.request.session.get('categories', [])
			self.fields['categories'].choices = [(str(c['id']), c['name']) for c in categories]  # Convert IDs to strings

			# If selected_categories are provided, convert them to strings for compatibility
			if selected_categories is not None:
				self.initial['categories'] = [str(cat_id) for cat_id in selected_categories]

	def save_to_session(self, request, post_id=None):
		# Save the form data to session manually, creating a post object
		posts = request.session.get('posts', [])
		if post_id:
			for post in posts:
				if post['id'] == post_id:
					post['title'] = self.cleaned_data['title']
					post['content'] = self.cleaned_data['content']
					post['categories'] = self.cleaned_data['categories']
					break
		else:
			post = {
				'id': post_id or len(posts) + 1,
				'title': self.cleaned_data['title'],
				'content': self.cleaned_data['content'],
				'categories': self.cleaned_data['categories'],
			}
			posts.append(post)
		request.session['posts'] = posts

		return post['id'] if post_id == None else post_id


class CategoryForm(forms.Form):
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
		'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500',
		'placeholder': 'Zadejte název kategorie'
	}))

	def save_to_session(self, request, category_id=None):
		categories = request.session.get('categories', [])

		if category_id:
			for category in categories:
				if category['id'] == category_id:
					category['name'] = self.cleaned_data['name']
					break
		else:
			category = {
				'id': len(categories) + 1 if categories else 1,
				'name': self.cleaned_data['name'],
			}
			categories.append(category)

		request.session['categories'] = categories

		return category['id'] if category_id == None else category_id
