from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from django.shortcuts import render, redirect

from users.forms.CustomUserRegistrationForm import CustomUserCreationForm


def register(request: HttpRequest) -> HttpResponse:
	if request.method == "POST":
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Uživatel úspěšně vytvořen')
			return redirect("users:login")
	else:
		form = CustomUserCreationForm()

	return render(request, "users/register.html", {
		"form": form
	})


def login(request: HttpRequest) -> HttpResponse:
	return render(request, "users/login.html")
