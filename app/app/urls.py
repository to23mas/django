from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('homepage.urls')),
    path("hello_world", include("hello_world.urls")),
    path("habit_tracker_1/", include("habit_tracker_1.urls")),
    path("habit_tracker_2/", include("habit_tracker_2.urls")),
    path('blog_1/', include('blog_1.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]
