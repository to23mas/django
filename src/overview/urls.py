"""URLS"""
from django.urls import path
from . import views

app_name = 'overview'
urlpatterns = [
    path("", views.overview, name="overview"),
    path("open", views.open, name="open"),
    path("done", views.done, name="done"),
    path("lock", views.lock, name="lock"),
]
