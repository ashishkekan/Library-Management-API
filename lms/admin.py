from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from lms.models import Author, Book, BookReview, BorrowRequest, Genre, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (("Role Info", {"fields": ("role",)}),)
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "role")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "available_copies", "total_copies")
    list_filter = ("genres", "author")
    search_fields = ("title", "isbn")
    filter_horizontal = ("genres",)


@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "user",
        "status",
        "requested_at",
        "approved_at",
        "returned_at",
    )
    list_filter = ("status", "requested_at")
    search_fields = ("user__username", "book__title")


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "rating", "rate")
    list_filter = ("rating", "rate")
    search_fields = ("user__username", "book__title")
