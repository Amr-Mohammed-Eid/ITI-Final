from django.shortcuts import render


def book_list(request):
    books = []
    return render(request, 'catalog/book_list.html', {'books': books})
