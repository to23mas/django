"""
URL configuration for inpv project.
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', include('overview.urls')),
    path('projects/', include('projects.urls')),

    path('accounts/login/', LoginView.as_view(redirect_authenticated_user=True)),
    path('logout/', LogoutView.as_view(), name='logout'),
]
