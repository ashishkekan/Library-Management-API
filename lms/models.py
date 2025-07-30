from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from lms.enums import BorrowStatus, UserRole


class User(AbstractUser):
    role = models.CharField(
        max_length=10, choices=UserRole.choices, default=UserRole.STUDENT
    )


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genres = models.ManyToManyField(Genre, related_name="books")
    isbn = models.CharField(max_length=13, unique=True)
    available_copies = models.PositiveIntegerField()
    total_copies = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class BorrowRequest(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="boorow_requests"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="boorow_requests"
    )
    status = models.CharField(
        max_length=10, choices=BorrowStatus.choices, default=BorrowStatus.PENDING
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}: {self.book.title} - {self.status}"


class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    rate = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.book.title} - {self.rating}"
