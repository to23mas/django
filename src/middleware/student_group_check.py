from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class GroupCheckMiddleware(MiddlewareMixin):
	def process_request(self, request):
		unverified_url = "/users/unverified/"
		login_url = "/users/login/"  # Update this if your login URL is different

		if request.path == unverified_url:
			if not request.user.is_authenticated:
				return redirect(login_url)
			if request.user.groups.filter(name="students").exists():
				return redirect(reverse('courses:overview'))
			return None

		if request.path.startswith('/admin/') or request.path.startswith('/users/'):
			return None

		if not request.user.is_authenticated:
			return redirect(login_url)

		if not request.user.groups.filter(name="students").exists():
			return redirect(unverified_url)

		return None
