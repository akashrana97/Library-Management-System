from django.contrib import admin

from .models import Author, Genre, Book, BorrowRequest, BookReview


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'ISBN', 'available_copies', 'total_copies')
    search_fields = ('title', 'author__name', 'ISBN')


@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'status', 'requested_at', 'approved_at', 'returned_at')
    search_fields = ('book__title', 'user__username', 'status')


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    search_fields = ('book__title', 'user__username', 'comment')
