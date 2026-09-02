from django.contrib import admin

from .models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_at', 'returned_at', 'is_active')
    list_filter = ('returned_at', 'borrowed_at')
    search_fields = ('user__username', 'book__title')
