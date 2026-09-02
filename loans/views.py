from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from catalog.models import Book  # موجود دلوقتي بعد دمج main
from .models import Loan

@login_required
def my_loans(request):
    loans = Loan.objects.filter(user=request.user)
    return render(request, 'loans/my_loans.html', {'loans': loans})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.available_copies < 1:
        messages.error(request, f"Sorry, '{book.title}' is not available.")
        return redirect('home')
    Loan.objects.create(user=request.user, book=book)
    book.available_copies -= 1
    book.save()
    messages.success(request, f"You borrowed '{book.title}'.")
    return redirect('loans:my_loans')

@login_required
def return_book(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, user=request.user, returned_at__isnull=True)
    loan.returned_at = timezone.now()
    loan.save()
    book = loan.book
    book.available_copies += 1
    book.save()
    messages.success(request, f"You returned '{book.title}'.")
    return redirect('loans:my_loans')