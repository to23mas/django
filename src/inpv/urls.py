"""
URL configuration for inpv project.
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

urlpatterns = [
	# admin
	path('admin/content/', include('content.urls')),
	path('admin/', admin.site.urls),
	# projects
	path('projects/', include('projects.urls')),
	#tests
	path('tests/', include('tests.urls')),
	#users
	path('users/', include('users.urls')),
	path('logout/', LogoutView.as_view(), name='logout'),
	#courses
	path('', include('courses.urls')),
]
