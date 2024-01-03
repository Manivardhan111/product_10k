# tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class YourAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

    def test_forgot_password(self):
        # Simulate a POST request to the forgot_password view
        response = self.client.post('/forgot_password/', {'email': 'test@example.com', 'otp': '123456', 'new_password': 'newpass'})

        # Assert that the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), 'Password reset successfully.')

        # Check that the user's password has been updated
        self.assertTrue(User.objects.get(username='testuser').check_password('newpass'))

    def test_change_password(self):
        # Log in the user
        self.client.login(username='testuser', password='password')

        # Simulate a POST request to the change_password view
        response = self.client.post('/change_password/', {'current_password': 'password', 'new_password': 'newpass', 'confirm_new_password': 'newpass'})

        # Assert that the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('utf-8'), 'change password')

        # Check that the user's password has been updated
        self.assertTrue(User.objects.get(username='testuser').check_password('newpass'))