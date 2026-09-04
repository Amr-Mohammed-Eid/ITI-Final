from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from catalog.models import Book


class CatalogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reader', password='Password123!', email='reader@example.com')
        self.book = Book.objects.create(
            title='Principles of Quantum Dynamics',
            author='Dr. Elias Vance',
            isbn='9780123456789',
            category='Physics',
            total_copies=5,
            available_copies=2,
        )

    def test_book_model_str(self):
        self.assertEqual(str(self.book), 'Principles of Quantum Dynamics')

    def test_catalog_view_requires_login(self):
        response = self.client.get(reverse('catalog:book_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('catalog:book_list')}")

    def test_catalog_view_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('catalog:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_list.html')
        self.assertIn(self.book, response.context['books'])
        self.assertContains(response, 'catalog-search-input')
        self.assertContains(response, 'catalog-search.js')
