from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import RegisterView, CustomLoginView

app_name = 'users'

urlpatterns = [
	path('register/', RegisterView.as_view(), name='register'),  # Registration page
	path('login/', CustomLoginView.as_view(), name='login'),      # Login page
	path('logout/', LogoutView.as_view(), name='logout'),
]

