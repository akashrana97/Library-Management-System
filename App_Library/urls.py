from django.urls import path
from App_Library.views import (
    BookListCreateView, BookDetailView,
    AuthorListCreateView, AuthorDetailView,
    GenreListCreateView, GenreDetailView,
    BorrowRequestListCreateView, BorrowRequestApproveView, BorrowRequestRejectView, BorrowRequestReturnView,
    BookReviewListCreateView, BookReviewDetailView
)

urlpatterns = [
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    path('genres/', GenreListCreateView.as_view(), name='genre-list-create'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),

    path('borrow/', BorrowRequestListCreateView.as_view(), name='borrow-request-list-create'),
    path('borrow/<int:pk>/approve/', BorrowRequestApproveView.as_view(), name='borrow-request-approve'),
    path('borrow/<int:pk>/reject/', BorrowRequestRejectView.as_view(), name='borrow-request-reject'),
    path('borrow/<int:pk>/return/', BorrowRequestReturnView.as_view(), name='borrow-request-return'),

    path('books/<int:book_pk>/reviews/', BookReviewListCreateView.as_view(), name='book-review-list-create'),
    path('books/<int:book_pk>/reviews/<int:pk>/', BookReviewDetailView.as_view(), name='book-review-detail'),
]
