# app/tests/test_authentication.py

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import User  

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )

    def test_login(self):
        url = reverse('api_token_auth')  # Ensure this is the correct URL name as defined in your project's urls.py
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
