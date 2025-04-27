from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'users'

urlpatterns = [
	path('register/', views.register, name="register"),
	path('login/', views.login_view, name="login"),
	path('unverified/', views.unverified_user, name='unverified_user'),
	path('verify_user/<str:code>/', views.verify_user, name='verify_user'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('forgot-password/', views.forgot_password, name='forgot_password'),
	path('reset-password/<str:code>/', views.reset_password, name='reset_password'),
]
