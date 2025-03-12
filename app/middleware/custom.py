from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponseNotFound


class LoginRequiredMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		excluded_urls = [settings.LOGIN_URL, settings.REGISTER_URL]

		if not request.user.is_authenticated and request.path not in excluded_urls:
			return redirect(settings.LOGIN_URL)

		return self.get_response(request)


class Redirect404Middleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)

		if isinstance(response, HttpResponseNotFound):
			if not request.user.is_authenticated:
				return redirect(settings.LOGIN_URL)
			return redirect('/')

		return response
