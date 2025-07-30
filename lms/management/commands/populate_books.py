import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from lms.models import Author, Book, BookReview, BorrowRequest, Genre

first_names = [
    "Aarav",
    "Priya",
    "Vikram",
    "Ananya",
    "Rohan",
    "Sneha",
    "Arjun",
    "Kavya",
    "Siddharth",
    "Neha",
]
last_names = [
    "Sharma",
    "Patel",
    "Verma",
    "Singh",
    "Gupta",
    "Mehta",
    "Kumar",
    "Joshi",
    "Reddy",
    "Iyer",
]
authors_data = [
    {
        "name": "Rabindranath Tagore",
        "bio": "Nobel laureate and author of Gitanjali",
    },
    {"name": "R.K. Narayan", "bio": "Renowned for Malgudi Days"},
    {"name": "Jhumpa Lahiri", "bio": "Pulitzer Prize-winning author"},
    {"name": "Amrita Pritam", "bio": "Famous Punjabi poet and novelist"},
]


class Command(BaseCommand):
    help = "Populates the database with dummy data for users, authors, genres, books, borrow requests, and reviews"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        users = []
        for i in range(7):
            role = "STUDENT" if i < 5 else "LIBRARIAN"
            username = f"{first_names[i]}{last_names[i].lower()}"
            email = f"{username}@example.com"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "role": role,
                    "first_name": first_names[i],
                    "last_name": last_names[i],
                },
            )
            if created:
                user.set_password("password123")
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Created user: {username} ({role})")
                )
            users.append(user)

        authors = []
        for data in authors_data:
            author, created = Author.objects.get_or_create(
                name=data["name"], defaults={"bio": data["bio"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created author: {data["name"]}'))
            authors.append(author)

        genres_data = ["Fiction", "Poetry", "Non-Fiction", "Historical", "Mythology"]
        genres = []
        for name in genres_data:
            genre, created = Genre.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created genre: {name}"))
            genres.append(genre)

        books_data = [
            {
                "title": "Gitanjali",
                "author": authors[0],
                "isbn": "978-0140449884",
                "total_copies": 5,
                "available_copies": 5,
            },
            {
                "title": "Malgudi Days",
                "author": authors[1],
                "isbn": "978-0143039655",
                "total_copies": 3,
                "available_copies": 3,
            },
            {
                "title": "The Namesake",
                "author": authors[2],
                "isbn": "978-0395927212",
                "total_copies": 4,
                "available_copies": 4,
            },
            {
                "title": "Pinjar",
                "author": authors[3],
                "isbn": "978-8129119551",
                "total_copies": 2,
                "available_copies": 2,
            },
            {
                "title": "The Guide",
                "author": authors[1],
                "isbn": "978-0143039648",
                "total_copies": 3,
                "available_copies": 3,
            },
        ]
        books = []
        for data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=data["isbn"],
                defaults={
                    "title": data["title"],
                    "author": data["author"],
                    "total_copies": data["total_copies"],
                    "available_copies": data["available_copies"],
                },
            )
            if created:
                book.genres.set(random.sample(genres, k=random.randint(1, 3)))
                book.save()
                self.stdout.write(self.style.SUCCESS(f'Created book: {data["title"]}'))
            books.append(book)

        statuses = ["PENDING", "APPROVED", "REJECTED", "RETURNED"]
        for student in users[:5]:
            for _ in range(random.randint(1, 3)):
                book = random.choice(books)
                status = random.choice(statuses)
                borrow_request = BorrowRequest.objects.create(
                    user=student,
                    book=book,
                    status=status,
                    requested_at=timezone.now()
                    - timezone.timedelta(days=random.randint(1, 30)),
                )
                if status == "APPROVED":
                    borrow_request.approved_at = (
                        borrow_request.requested_at + timezone.timedelta(days=1)
                    )
                    borrow_request.book.available_copies = max(
                        0, borrow_request.book.available_copies - 1
                    )
                    borrow_request.book.save()
                elif status == "RETURNED":
                    borrow_request.approved_at = (
                        borrow_request.requested_at + timezone.timedelta(days=1)
                    )
                    borrow_request.returned_at = (
                        borrow_request.approved_at
                        + timezone.timedelta(days=random.randint(1, 10))
                    )
                borrow_request.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created borrow request: {student.username} - {book.title} ({status})"
                    )
                )

        review_comments = [
            "A beautifully written book!",
            "Really enjoyed the storyline.",
            "Could have been more engaging.",
            "A classic masterpiece!",
            "Highly recommended for all readers.",
        ]
        for student in users[:5]:
            for _ in range(random.randint(1, 2)):
                book = random.choice(books)
                BookReview.objects.create(
                    user=student,
                    book=book,
                    rating=random.randint(1, 5),
                    comment=random.choice(review_comments),
                    created_at=timezone.now()
                    - timezone.timedelta(days=random.randint(1, 30)),
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created review by {student.username} for {book.title}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Successfully populated dummy data!"))
