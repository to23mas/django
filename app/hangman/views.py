from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.static import serve
from django.conf import settings
import random

# List of words for the game
WORDS = [
    "PYTHON", "DJANGO", "JAVASCRIPT", "HTML", "CSS",
    "DATABASE", "FRAMEWORK", "CODING", "DEVELOPER",
    "PROGRAMMING", "WEB", "APPLICATION", "SOFTWARE",
    "COMPUTER", "ALGORITHM"
]

def index(request):
    # Don't redirect, serve the file directly
    return serve(request, 'hangman/index.html', document_root=settings.STATICFILES_DIRS[0])

def get_word(request):
    # Get a random word from our list
    random_word = random.choice(WORDS)
    # Return JSON response
    return JsonResponse({'word': random_word})
