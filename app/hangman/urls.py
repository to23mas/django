from django.urls import path
from . import views

app_name = 'hangman'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/hangman/word/', views.get_word, name='get_word'),
]