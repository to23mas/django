"""routing for courses"""

from django.urls import path

from .views import *

app_name = 'courses'

urlpatterns = [
	path("", overview, name="overview"),
	path("unlock/<int:course_id>", enroll, name="enroll"),
]
