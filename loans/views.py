from django.shortcuts import render


def my_loans(request):
    loans = []
    return render(request, 'loans/my_loans.html', {'loans': loans})
