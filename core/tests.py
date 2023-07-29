from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser

class CustomUserModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test_user', email='test@example.com', password='test_password'
        )

    def test_custom_user_model_str(self):
        self.assertEqual(str(self.user), 'test_user')

class CustomUserRegistrationTestCase(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'test_password',
            'confirm_password': 'test_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'test_user')

    def test_register_user_with_missing_fields(self):
        url = reverse('register')
        data = {
            'username': 'test_user',
            'password': 'test_password',
            'confirm_password': 'test_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_with_non_matching_passwords(self):
        url = reverse('register')
        data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'test_password',
            'confirm_password': 'wrong_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CustomUserLoginTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test_user', email='test@example.com', password='test_password'
        )

    def test_login_user(self):
        url = reverse('login')
        data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)

    def test_login_user_with_invalid_credentials(self):
        url = reverse('login')
        data = {
            'username': 'test_user',
            'password': 'wrong_password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
