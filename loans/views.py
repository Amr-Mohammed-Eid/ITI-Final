from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Loan

@login_required
def my_loans(request):
    loans = Loan.objects.filter(user=request.user)
    return render(request, 'loans/my_loans.html', {'loans': loans})

@login_required
def borrow_book(request, book_id):
    # مؤقتاً: بنستقبل book_id ونعمل Loan بعنوان الكتاب
    book_title = f"Book #{book_id}"  # أو ممكن تيجي من ريكويست
    Loan.objects.create(user=request.user, book_title=book_title)
    messages.success(request, f"You borrowed '{book_title}'.")
    return redirect('loans:my_loans')

@login_required
def return_book(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id, user=request.user, returned_at__isnull=True)
    loan.returned_at = timezone.now()
    loan.save()
    messages.success(request, f"You returned '{loan.book_title}'.")
    return redirect('loans:my_loans')