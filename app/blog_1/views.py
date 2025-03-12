from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category
from .forms import PostForm, CategoryForm

def post_list(request):
	posts = Post.objects.all().order_by('-created_at')
	categories = Category.objects.all()
	category_filter = request.GET.get('category')

	if category_filter:
		posts = posts.filter(categories__id=category_filter)

	return render(request, 'blog_1/post_list.html', {
		'posts': posts,
		'categories': categories,
	})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog_1/post_detail.html', {'post': post})

def post_create(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('blog_1:post_list')
	else:
		form = PostForm()
	return render(request, 'blog_1/post_form.html', {'form': form})

def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			form.save()
			return redirect('blog_1:post_edit', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog_1/post_form.html', {
		'form': form,
		'post': post,
	})


def post_delete(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('blog_1:post_list')

#---------

def category_list(request):
	categories = Category.objects.all()

	return render(request, 'blog_1/category_list.html', {
		'categories': categories,
	})

def category_detail(request, pk):
	category = get_object_or_404(Category, name=pk)
	return render(request, 'blog_1/category_detail.html', {'category': category})

def category_create(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			category = form.save()
			return redirect('blog_1:category_edit', category.id)
	else:
		form = CategoryForm()

	categories = Category.objects.all()
	return render(request, 'blog_1/category_form.html', {
		'form': form,
		'categories': categories,
	})

def category_edit(request, id):
	category = get_object_or_404(Category, id=id)
	print(category)
	if request.method == 'POST':
		form = CategoryForm(request.POST, instance=category)
		if form.is_valid():
			form.save()
			return redirect('blog_1:category_edit', id=category.id)
	else:
		form = CategoryForm(instance=category)
	return render(request, 'blog_1/category_form.html', {
		'form': form,
		'category': category,
	})

def category_delete(request, id):
	category = get_object_or_404(Category, id=id)
	category.delete()
	return redirect('blog_1:category_list')
