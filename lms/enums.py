from django.db import models


class UserRole(models.TextChoices):
    STUDENT = "STUDENT", "Student"
    LIBRARIAN = "LIBRARIAN", "Librarian"


class BorrowStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    RETURNED = "RETURNED", "Returned"
