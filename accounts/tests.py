from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm


class AuthBackendTests(TestCase):
    def test_signup_get_renders_template_with_form(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertIsInstance(response.context['form'], SignUpForm)

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
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertIsInstance(response.context['form'], SignUpForm)
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(User.objects.filter(username='bob').exists())

    def test_login_get_renders_template_with_form(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

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

    def test_login_invalid_post_rerenders_template(self):
        response = self.client.post(
            reverse('login'),
            {'username': 'nonexistent', 'password': 'wrongpassword'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)
        self.assertTrue(response.context['form'].errors)

    def test_login_next_url_redirect(self):
        User.objects.create_user(username='dave', password='StrongPass123!')
        response = self.client.post(
            reverse('login') + '?next=/some/next/path/',
            {'username': 'dave', 'password': 'StrongPass123!'},
        )
        self.assertRedirects(response, '/some/next/path/', fetch_redirect_response=False)

    def test_authenticated_user_redirects(self):
        user = User.objects.create_user(username='eve', password='StrongPass123!')
        self.client.force_login(user)
        signup_response = self.client.get(reverse('signup'))
        self.assertRedirects(signup_response, reverse('home'))
        login_response = self.client.get(reverse('login'))
        self.assertRedirects(login_response, reverse('home'))

    def test_logout_rejects_get(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 405)
