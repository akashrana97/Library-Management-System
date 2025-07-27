from rest_framework import serializers
from .models import Author, Genre, Book, BorrowRequest, BookReview


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)  #
    genres = GenreSerializer(many=True, read_only=True)  #
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), write_only=True, source='author')
    genre_ids = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(), many=True, write_only=True,
                                                   source='genres')

    class Meta:
        model = Book
        fields = '__all__'


class BorrowRequestSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = BorrowRequest
        fields = '__all__'
        read_only_fields = ('status', 'approved_at', 'returned_at')


class BookReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = BookReview
        fields = '__all__'
        read_only_fields = ('user', 'book')
