from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('homepage.urls')),
    path("hello_world", include("hello_world.urls")),
    path("habit_tracker_1/", include("habit_tracker_1.urls")),
]
