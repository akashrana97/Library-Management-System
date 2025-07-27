from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import BorrowRequest, Book

@receiver(post_save, sender=BorrowRequest)
def update_book_copies_on_borrow_request(sender, instance, **kwargs):
    if instance.status == 'APPROVED' and not instance.returned_at:
        book = instance.book
        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()
    elif instance.status == 'RETURNED' and instance.returned_at:
        book = instance.book
        book.available_copies += 1
        book.save()