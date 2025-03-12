from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import RegisterForm, CustomLoginForm

class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')  # Redirect to the login page after successful registration

    def form_valid(self, form):
        form.save()  # Save the new user
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'users/login.html'  # Custom template for login
    form_class = CustomLoginForm

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
