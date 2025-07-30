from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from lms.views import (
    AuthorListCreateView,
    BookDetailView,
    BookListCreateView,
    BookReviewDetailView,
    BookReviewListCreateView,
    BorrowRequestActionView,
    BorrowRequestCreateView,
    BorrowRequestListView,
    GenreListCreateView,
    UserRegisterView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Library Management System API",
        default_version="v1",
        description="API for managing books, authors, genres, borrow requests, and reviews",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("api/register/", UserRegisterView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/books/", BookListCreateView.as_view(), name="book-list"),
    path("api/books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("api/authors/", AuthorListCreateView.as_view(), name="author-list"),
    path("api/genres/", GenreListCreateView.as_view(), name="genre-list"),
    path("api/borrow/", BorrowRequestCreateView.as_view(), name="borrow-request"),
    path("api/borrow/me/", BorrowRequestListView.as_view(), name="borrow-list"),
    path(
        "api/borrow/<int:pk>/approve/",
        BorrowRequestActionView.as_view(),
        name="borrow-approve",
    ),
    path(
        "api/borrow/<int:pk>/reject/",
        BorrowRequestActionView.as_view(),
        name="borrow-reject",
    ),
    path(
        "api/borrow/<int:pk>/return/",
        BorrowRequestActionView.as_view(),
        name="borrow-return",
    ),
    path(
        "api/books/<int:book_id>/reviews/",
        BookReviewListCreateView.as_view(),
        name="review-list",
    ),
    path("api/reviews/<int:pk>/", BookReviewDetailView.as_view(), name="review-detail"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
