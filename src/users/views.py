import hashlib
import os
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User, Group
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from brevo.brevo import send_registration_email, send_password_reset_email
from users.forms.CustomUserCreationForm import CustomUserCreationForm


def register(request: HttpRequest) -> HttpResponse:
	# if os.getenv('REGISTRATION') == 'disabled':
	# 	return render(request, "users/register-disabled.html", {})

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
	user.is_staff = True
	user.save()
	login(request, user)

	messages.success(request, 'Registrace proběhla úspěšně')
	return redirect("courses:overview")

class ForgotPasswordForm(forms.Form):
	email = forms.EmailField(label='Email')

def forgot_password(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		form = ForgotPasswordForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			try:
				user = User.objects.get(email=email)
				data = f"{user.username}{user.email}"
				reset_hash = hashlib.sha256(data.encode()).hexdigest()
				reset_url = request.build_absolute_uri(reverse('users:reset_password', kwargs={'code': reset_hash}))
				user.last_name = reset_hash
				user.save()

				if send_password_reset_email(user.username, email, reset_url):
					messages.success(request, 'Email s instrukcemi pro obnovení hesla byl odeslán.')
				else:
					messages.error(request, 'Nepodařilo se odeslat email. Prosím zkuste to později.')
				return redirect('users:login')
			except User.DoesNotExist:
				messages.error(request, 'Uživatel s tímto emailem nebyl nalezen.')
	else:
		form = ForgotPasswordForm()

	return render(request, "users/forgot_password.html", {
		"form": form
	})

def reset_password(request: HttpRequest, code: str) -> HttpResponse:
	if code == '':
		return redirect("users:login")

	try:
		user = User.objects.get(last_name=code)
	except User.DoesNotExist:
		messages.error(request, 'Neplatný odkaz pro obnovení hesla.')
		return redirect("users:login")

	if request.method == "POST":
		form = SetPasswordForm(user, request.POST)
		if form.is_valid():
			form.save()
			user.last_name = ''
			user.save()
			messages.success(request, 'Heslo bylo úspěšně změněno.')
			return redirect("users:login")
	else:
		form = SetPasswordForm(user)

	return render(request, "users/reset_password.html", {
		"form": form
	})
