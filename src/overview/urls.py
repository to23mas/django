"""URLS"""
from django.urls import path

from . import views

app_name = 'login'
urlpatterns = [
    path("", views.Overview.as_view(), name="overview"),
]
