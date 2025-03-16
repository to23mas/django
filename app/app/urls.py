from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('homepage.urls')),
    path("hello_world", include("hello_world.urls")),
    path("habit_tracker_1/", include("habit_tracker_1.urls")),
    path("habit_tracker_2/", include("habit_tracker_2.urls")),
    path('blog_1/', include('blog_1.urls')),
    path('users/', include('users.urls')),
    path("birthdays/", include("birthdays.urls")),
    path("chat/", include("chat.urls")),
    path('library/', include('library.urls', namespace='library')),
    # path("__reload__/", include("django_browser_reload.urls")),
]
