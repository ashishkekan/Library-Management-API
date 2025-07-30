from rest_framework import serializers

from lms.models import Author, Book, BookReview, BorrowRequest, Genre, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BorrowRequestSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source="book", write_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )

    class Meta:
        model = BorrowRequest
        fields = "__all__"


class BookReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BookReview
        fields = "__all__"
