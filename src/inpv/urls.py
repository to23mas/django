"""
URL configuration for inpv project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
	# admin
	path('admin/content/', include('content.urls')),
	path('admin/', admin.site.urls),
	# projects lessons chapters
	path('projects/', include('projects.urls')),
	path('projects/', include('lessons.urls')),
	path('projects/', include('user_progress.urls')),
	#tests
	path('tests/', include('tests.urls')),
	#demos
	path('demos/', include('demos.urls')),
	#users
	path('users/', include('users.urls')),
	#courses
	path('', include('courses.urls')),
]
