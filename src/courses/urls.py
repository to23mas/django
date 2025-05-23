"""routing for courses"""

from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
	path("", views.overview, name="overview"),
	path("unlock/<str:course_id>", views.enroll, name="enroll"),
]
