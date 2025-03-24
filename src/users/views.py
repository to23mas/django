import hashlib
import os
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse

from brevo.brevo import send_registration_email
from users.forms.CustomUserCreationForm import CustomUserCreationForm


def register(request: HttpRequest) -> HttpResponse:
	if os.getenv('REGISTRATION') == 'disabled':
		return render(request, "users/register-disabled.html", {})

	if request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			anon_user = form.save(commit=False)

			data = f"{anon_user.username}{anon_user.email}"
			registration_hash = hashlib.sha256(data.encode()).hexdigest()
			verify_url = request.build_absolute_uri(reverse('users:verify_user', kwargs={'code': registration_hash}))
			anon_user.last_name = registration_hash
			anon_user.save()

			send_registration_email(anon_user.username, form.cleaned_data['email'], verify_url)
			return redirect("courses:overview")
	else:
		form = CustomUserCreationForm()

	return render(request, "users/register.html", {
		"form": form
	})


def login_view(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			login(request, form.get_user())
			return redirect("courses:overview")
	else:
		form = AuthenticationForm()

	return render(request, "users/login.html", {
		"form": form
	})

def unverified_user(request: HttpRequest) -> HttpResponse:
	email = request.user.email #type: ignore
	return render(request, "users/unverified.html", {'email': email})

def verify_user(request: HttpRequest, code: str) -> HttpResponse:

	if code == '':
		return redirect("user:login")

	try:
		user = User.objects.get(last_name=code)
		students_group, _ = Group.objects.get_or_create(name="students")
		user.groups.add(students_group)
	except Exception:
		user = None

	if user is None:
		return redirect("user:login")

	user.last_name = ''
	user.save()
	login(request, user)

	messages.success(request, 'Registrace proběhla úspěšně')
	return redirect("courses:overview")
