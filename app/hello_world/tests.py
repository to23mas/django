from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class HelloWorldTests(TestCase):
    def setUp(self):
        """Set up test client and create test user"""
        self.client = Client()
        self.url = reverse('hello_world:hello_world')
        # Create and login a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_view_exists(self):
        """Test if the view exists and returns 200 OK"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_returns_text(self):
        """Test if the view returns text content"""
        response = self.client.get(self.url)
        self.assertIsInstance(response.content.decode(), str)

    def test_view_not_empty(self):
        """Test if the response is not empty"""
        response = self.client.get(self.url)
        self.assertTrue(len(response.content) > 0)

    def test_view_uses_get(self):
        """Test if the view responds to GET request"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_requires_login(self):
        """Test if the view requires authentication"""
        # Create a new client without logging in
        client = Client()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_logout_then_access(self):
        """Test access after logout"""
        # First verify we can access
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        # Then logout
        self.client.logout()
        
        # Verify we can't access anymore
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_invalid_credentials(self):
        """Test access with invalid login credentials"""
        client = Client()
        # Try to login with wrong password
        logged_in = client.login(username='testuser', password='wrongpassword')
        self.assertFalse(logged_in)
        
        # Verify access is denied
        response = client.get(self.url)
        self.assertEqual(response.status_code, 302)
    
