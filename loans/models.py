from django.db import models
from django.conf import settings

class Loan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='loans'
    )
    book_title = models.CharField(max_length=200)  # مؤقت، بدل ForeignKey للكتاب
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-borrowed_at']

    def __str__(self):
        return f"{self.user.username} - {self.book_title}"

    @property
    def is_active(self):
        return self.returned_at is None