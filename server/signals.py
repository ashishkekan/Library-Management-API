from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from lms.models import BorrowRequest


@receiver(post_save, sender=BorrowRequest)
def update_books(sender, instance, **kwargs):
    if instance.status == "Approved" and instance.approved_at is None:
        instance.book.available_copies -= 1
        instance.book.save()
        instance.approved_at = timezone.now()
        instance.save()
    elif instance.status == "Returned" and instance.returned_at is None:
        instance.book.available_copies += 1
        instance.book.save()
        instance.returned_at = timezone.now()
        instance.save()
