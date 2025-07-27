from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import transaction
from django.utils import timezone

from .models import Author, Genre, Book, BorrowRequest, BookReview
from .serializers import (
    AuthorSerializer, GenreSerializer,
    BookSerializer, BorrowRequestSerializer, BookReviewSerializer
)
from .permissions import IsLibrarian, IsOwnerOrReadOnly


class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsLibrarian]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarian]


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'genres']
    search_fields = ['title', 'author__name', 'genres__name', 'ISBN']
    ordering_fields = ['title', 'author__name', 'available_copies']

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsLibrarian]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsLibrarian]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsLibrarian]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsLibrarian]


class BorrowRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = BorrowRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'LIBRARIAN':
            return BorrowRequest.objects.all()
        return BorrowRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.role != 'STUDENT':
            raise serializers.ValidationError("Only students can request to borrow books.")
        serializer.save(user=self.request.user, status='PENDING')


class BorrowRequestApproveView(APIView):
    permission_classes = [IsLibrarian]

    def patch(self, request, pk, format=None):
        try:
            borrow_request = BorrowRequest.objects.get(pk=pk)
        except BorrowRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if borrow_request.status == 'PENDING':
            with transaction.atomic():
                book = borrow_request.book
                if book.available_copies > 0:
                    borrow_request.status = 'APPROVED'
                    borrow_request.approved_at = timezone.now()
                    borrow_request.save()
                    return Response({'status': 'borrow request approved'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'No available copies of this book.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Borrow request cannot be approved'}, status=status.HTTP_400_BAD_REQUEST)


class BorrowRequestRejectView(APIView):
    permission_classes = [IsLibrarian]

    def patch(self, request, pk, format=None):
        try:
            borrow_request = BorrowRequest.objects.get(pk=pk)
        except BorrowRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if borrow_request.status == 'PENDING':
            borrow_request.status = 'REJECTED'
            borrow_request.save()
            return Response({'status': 'borrow request rejected'}, status=status.HTTP_200_OK)
        return Response({'error': 'Borrow request cannot be rejected'}, status=status.HTTP_400_BAD_REQUEST)


class BorrowRequestReturnView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, format=None):
        try:
            borrow_request = BorrowRequest.objects.get(pk=pk)
        except BorrowRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not (request.user == borrow_request.user or request.user.role == 'LIBRARIAN'):
            return Response({'error': 'You do not have permission to perform this action.'},
                            status=status.HTTP_403_FORBIDDEN)

        if borrow_request.status == 'APPROVED':
            with transaction.atomic():
                borrow_request.status = 'RETURNED'
                borrow_request.returned_at = timezone.now()
                borrow_request.save()
                return Response({'status': 'book marked as returned'}, status=status.HTTP_200_OK)
        return Response({'error': 'Book cannot be marked as returned from its current state'},
                        status=status.HTTP_400_BAD_REQUEST)


class BookReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        book_id = self.kwargs['book_pk']
        return BookReview.objects.filter(book_id=book_id)

    def perform_create(self, serializer):
        book_id = self.kwargs['book_pk']
        book = generics.get_object_or_404(Book, pk=book_id)
        serializer.save(user=self.request.user, book=book)


class BookReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return BookReview.objects.none()
        book_id = self.kwargs['book_pk']
        return BookReview.objects.filter(book_id=book_id)