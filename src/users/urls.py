from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
	path('register/', views.register, name="register"),
	path('login/', views.login_view, name="login"),
	path('unverified/', views.unverified_user, name='unverified_user'),
	path('verify_user/<str:code>/', views.verify_user, name='verify_user'),
]
