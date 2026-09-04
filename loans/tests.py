from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from catalog.models import Book
from loans.models import Loan


class AcceptanceCriteriaTests(TestCase):
    """
    End-to-end acceptance criteria tests using Django test client:
    - Signup -> login -> browse/search catalog -> borrow book with available copies
    - Borrowing a book with zero available copies is blocked with a clear error message
    - Returning a book updates available-copy count immediately
    - Librarian can view/manage books and loans via /admin/
    """

    def setUp(self):
        # Create sample books
        self.available_book = Book.objects.create(
            title='Principles of Quantum Dynamics',
            author='Dr. Elias Vance',
            isbn='9780123456789',
            category='Physics',
            total_copies=5,
            available_copies=2,
        )
        self.unavailable_book = Book.objects.create(
            title='The Architecture of Modern Poetry',
            author='Sarah L. Jenkins',
            isbn='9780123456780',
            category='Literature',
            total_copies=3,
            available_copies=0,
        )

        # Create librarian (superuser/staff)
        self.librarian = User.objects.create_superuser(
            username='librarian',
            email='admin@warraq.edu',
            password='AdminPassword123!',
        )

    def test_signup_login_browse_borrow_flow(self):
        """
        AC 1: A member can sign up, log in, browse/search the catalog,
        and successfully borrow a book with available copies.
        """
        # Step 1: Member signs up
        signup_response = self.client.post(
            reverse('signup'),
            {
                'username': 'john_reader',
                'email': 'john@example.com',
                'password1': 'MemberPass123!',
                'password2': 'MemberPass123!',
            },
            follow=True,
        )
        self.assertEqual(signup_response.status_code, 200)
        self.assertTrue(User.objects.filter(username='john_reader').exists())

        # Step 2: Log out and log back in to verify login flow
        self.client.post(reverse('logout'))
        login_response = self.client.post(
            reverse('login'),
            {
                'username': 'john_reader',
                'password': 'MemberPass123!',
            },
            follow=True,
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(login_response.wsgi_request.user.is_authenticated)

        # Step 3: Browse catalog
        catalog_response = self.client.get(reverse('catalog:book_list'))
        self.assertEqual(catalog_response.status_code, 200)
        self.assertContains(catalog_response, 'Principles of Quantum Dynamics')
        self.assertContains(catalog_response, 'catalog-search-input')

        # Step 4: Borrow available book
        initial_available = self.available_book.available_copies
        borrow_response = self.client.get(
            reverse('loans:borrow_book', args=[self.available_book.id]),
            follow=True,
        )
        self.assertRedirects(borrow_response, reverse('loans:my_loans'))

        # Check DB updates: copies decremented by 1, loan created
        self.available_book.refresh_from_db()
        self.assertEqual(self.available_book.available_copies, initial_available - 1)

        loan = Loan.objects.filter(user__username='john_reader', book=self.available_book).first()
        self.assertIsNotNone(loan)
        self.assertTrue(loan.is_active)
        self.assertIsNone(loan.returned_at)

        # Verify success message rendered
        messages = list(borrow_response.context['messages'])
        self.assertTrue(any('You borrowed' in str(m) for m in messages))

    def test_borrow_book_zero_copies_blocked_with_error(self):
        """
        AC 2: Attempting to borrow a book with zero available copies is correctly
        blocked with a clear error message.
        """
        member = User.objects.create_user(username='jane_reader', password='MemberPass123!')
        self.client.force_login(member)

        # Attempt to borrow book with 0 available copies
        response = self.client.get(
            reverse('loans:borrow_book', args=[self.unavailable_book.id]),
            follow=True,
        )

        # Copies should remain 0
        self.unavailable_book.refresh_from_db()
        self.assertEqual(self.unavailable_book.available_copies, 0)

        # No loan created
        self.assertFalse(Loan.objects.filter(user=member, book=self.unavailable_book).exists())

        # Clear error message shown
        messages = list(response.context['messages'])
        self.assertTrue(any('is not available' in str(m) for m in messages))

    def test_return_book_updates_available_copies_immediately(self):
        """
        AC 3: A member can return a borrowed book and the available-copy count
        updates immediately.
        """
        member = User.objects.create_user(username='sam_reader', password='MemberPass123!')
        self.client.force_login(member)

        # Create active loan
        loan = Loan.objects.create(user=member, book=self.available_book)
        self.available_book.available_copies = 1
        self.available_book.save()

        # Return the book
        return_response = self.client.get(
            reverse('loans:return_book', args=[loan.id]),
            follow=True,
        )
        self.assertRedirects(return_response, reverse('loans:my_loans'))

        # Check DB updates: available_copies incremented immediately, loan is closed
        self.available_book.refresh_from_db()
        self.assertEqual(self.available_book.available_copies, 2)

        loan.refresh_from_db()
        self.assertFalse(loan.is_active)
        self.assertIsNotNone(loan.returned_at)

        # Verify success message rendered
        messages = list(return_response.context['messages'])
        self.assertTrue(any('You returned' in str(m) for m in messages))

    def test_librarian_admin_access(self):
        """
        AC 4: A librarian can view and manage books and loan records
        through the Django Admin site.
        """
        # Librarian logs in to admin
        self.client.force_login(self.librarian)

        # Can access admin dashboard
        admin_index = self.client.get('/admin/')
        self.assertEqual(admin_index.status_code, 200)

        # Can access and view books in admin
        admin_books = self.client.get('/admin/catalog/book/')
        self.assertEqual(admin_books.status_code, 200)
        self.assertContains(admin_books, 'Principles of Quantum Dynamics')

        # Can access and view loans in admin
        admin_loans = self.client.get('/admin/loans/loan/')
        self.assertEqual(admin_loans.status_code, 200)

    def test_regular_member_blocked_from_admin(self):
        """
        Non-staff members cannot access the librarian admin site.
        """
        member = User.objects.create_user(username='regular_member', password='MemberPass123!')
        self.client.force_login(member)

        response = self.client.get('/admin/')
        # Non-staff users get redirected to admin login
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
