from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock

class CourseViewsTest(TestCase):
	def setUp(self):
		# Create a test user
		self.client = Client()
		self.user = User.objects.create_user(username='testuser', password='testpass123')

		# URLs
		self.overview_url = reverse('courses:overview')
		self.enroll_url = reverse('courses:enroll', kwargs={'course_id': 'test-course'})
		self.login_url = '/users/login/'

	@patch('courses.views.CourseStorage')
	def test_enroll_page_with_invalid_course(self, mock_storage_class):
		"""Test enrollment with non-existent course"""
		# Setup mock
		mock_storage = MagicMock()
		mock_storage.get_course_by_id.return_value = None
		mock_storage_class.return_value = mock_storage

		# Login and test
		self.client.login(username='testuser', password='testpass123')
		response = self.client.get(self.enroll_url)
		self.assertRedirects(response, '/users/unverified/')

	def test_enroll_page_requires_login(self):
		"""Test that enrollment requires authentication"""
		response = self.client.get(self.enroll_url)
		self.assertRedirects(response, self.login_url)

	def test_overview_page_requires_login(self):
		"""Test that overview requires authentication"""
		response = self.client.get(self.overview_url)
		self.assertRedirects(response, self.login_url)
