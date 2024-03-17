"""URLS"""
from django.urls import path
from . import views

app_name = 'overview'
urlpatterns = [
    path("", views.overview, name="overview"),
]
