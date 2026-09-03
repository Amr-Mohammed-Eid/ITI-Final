import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import Book

SAMPLE_BOOKS = [
    {
        'title': 'Principles of Quantum Dynamics',
        'author': 'Dr. Elias Vance',
        'isbn': '9780123456789',
        'category': 'Physics',
        'total_copies': 5,
        'available_copies': 2,
    },
    {
        'title': 'The Architecture of Modern Poetry',
        'author': 'Sarah L. Jenkins',
        'isbn': '9780123456780',
        'category': 'Literature',
        'total_copies': 3,
        'available_copies': 0,
    },
    {
        'title': 'Advanced Algorithmic Structures',
        'author': 'T. Cormen et al.',
        'isbn': '9780123456781',
        'category': 'Computer Science',
        'total_copies': 12,
        'available_copies': 8,
    },
    {
        'title': 'The Fall of the Byzantine Empire',
        'author': 'Arthur Koestler',
        'isbn': '9780123456782',
        'category': 'History',
        'total_copies': 1,
        'available_copies': 1,
    },
]

def seed():
    created_count = 0
    for book_data in SAMPLE_BOOKS:
        book, created = Book.objects.get_or_create(
            isbn=book_data['isbn'],
            defaults=book_data
        )
        if created:
            created_count += 1
            print(f"Created book: {book.title}")
        else:
            print(f"Book already exists: {book.title}")
    print(f"Seeding complete. {created_count} new books created, total books: {Book.objects.count()}.")

if __name__ == '__main__':
    seed()
