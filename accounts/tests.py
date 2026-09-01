from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthBackendTests(TestCase):
    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse('signup'),
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='alice').exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_signup_rejects_invalid_payload(self):
        response = self.client.post(
            reverse('signup'),
            {
                'username': 'bob',
                'email': 'not-an-email',
                'password1': 'x',
                'password2': 'y',
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username='bob').exists())

    def test_login_and_logout(self):
        User.objects.create_user(username='carol', password='StrongPass123!')
        login_response = self.client.post(
            reverse('login'),
            {'username': 'carol', 'password': 'StrongPass123!'},
        )
        self.assertRedirects(login_response, reverse('home'))

        logout_response = self.client.post(reverse('logout'))
        self.assertRedirects(logout_response, reverse('login'))
        self.assertFalse(logout_response.wsgi_request.user.is_authenticated)

    def test_logout_rejects_get(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 405)
