from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from lms.models import Author, Book, BookReview, BorrowRequest, Genre, User
from lms.permissions import IsLibrarian, IsOwnerOrReadOnly, IsStudent
from lms.serializers import (
    AuthorSerializer,
    BookCreateSerializer,
    BookReviewSerializer,
    BookSerializer,
    BorrowRequestSerializer,
    GenreSerializer,
    UserSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class with default page size of 10.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class UserRegisterView(generics.CreateAPIView):
    """
    API view to register a new user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class BookListCreateView(generics.ListCreateAPIView):
    """
    API view to list all books or create a new book (librarian only).
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["author", "genres"]
    search_fields = ["title", "isbn"]
    ordering_fields = ["title", "available_copies"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookCreateSerializer
        return BookSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsLibrarian()]
        return [IsAuthenticated()]


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a single book.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return BookCreateSerializer
        return BookSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsLibrarian()]
        return [IsAuthenticated()]


class AuthorListCreateView(generics.ListCreateAPIView):
    """
    API view to list or create authors (create allowed for librarians only).
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsLibrarian()]
        return [IsAuthenticated()]


class GenreListCreateView(generics.ListCreateAPIView):
    """
    API view to list or create genres (create allowed for librarians only).
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsLibrarian()]
        return [IsAuthenticated()]


class BorrowRequestCreateView(generics.CreateAPIView):
    """
    API view to create a borrow request (students only).
    """

    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsStudent]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BorrowRequestListView(generics.ListAPIView):
    """
    API view to list borrow requests of the current user.
    """

    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BorrowRequest.objects.filter(user=self.request.user)


class BorrowRequestActionView(generics.UpdateAPIView):
    """
    API view to approve, reject, or return a borrow request (librarian only).
    """

    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsLibrarian]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = self.request.path.split("/")[-2]
        if action == "approve" and instance.status == "PENDING":
            instance.status = "APPROVED"
            instance.approved_at = timezone.now()
            instance.book.available_copies -= 1
            instance.book.save()
        elif action == "reject" and instance.status == "PENDING":
            instance.status = "REJECTED"
        elif action == "return" and instance.status == "APPROVED":
            instance.status = "RETURNED"
            instance.returned_at = timezone.now()
            instance.book.available_copies += 1
            instance.book.save()
        else:
            return Response(
                {"detail": "Invalid action or status"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance.save()
        return Response(self.get_serializer(instance).data)


class BookReviewListCreateView(generics.ListCreateAPIView):
    """
    API view to list or create reviews for a specific book.
    """

    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BookReview.objects.filter(book_id=self.kwargs["book_id"])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, book_id=self.kwargs["book_id"])


class BookReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a book review.
    """

    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]
