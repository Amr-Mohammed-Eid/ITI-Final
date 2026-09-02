from django.db import models
from django.conf import settings
from catalog.models import Book

class Loan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='loans'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='loans'
    )
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-borrowed_at']

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    @property
    def is_active(self):
        return self.returned_at is None