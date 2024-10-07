from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login
from django.shortcuts import render, redirect

from users.forms.CustomUserRegistrationForm import CustomUserCreationForm


def register(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			login(request, form.save())
			messages.success(request, 'Uživatel úspěšně vytvořen')
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
