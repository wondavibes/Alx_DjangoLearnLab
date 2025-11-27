from django.shortcuts import render
from rest_framework import generics, permissions, status, filters as drf_filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request as DRFRequest
from typing import cast
from django.db.models import QuerySet
from .models import Book
from .serializers import BookSerializer


# Generic views for Book CRUD operations
class BookListView(generics.ListAPIView):
    """Retrieve a list of all books."""

    permission_classes = [permissions.AllowAny]
    serializer_class = BookSerializer

    # Enable filtering, search and ordering. `DjangoFilterBackend` requires `django-filter`.
    filter_backends = []
    if DjangoFilterBackend is not None:
        filter_backends.append(DjangoFilterBackend)
    # SearchFilter lets clients use `?search=...`
    filter_backends.append(drf_filters.SearchFilter)
    # OrderingFilter lets clients use `?ordering=field` and `?ordering=-field`
    filter_backends.append(drf_filters.OrderingFilter)

    # Fields available for exact/contains filtering via DjangoFilterBackend
    filterset_fields = ["title", "author__name", "publication_year"]

    # Fields to search via DRF's SearchFilter (q=... query param)
    search_fields = ["title", "author__name"]

    # Fields clients may order by and default ordering
    ordering_fields = ["title", "publication_year", "author__name"]
    ordering = ["title"]

    def get_queryset(self) -> QuerySet[Book]:  # type: ignore[override]
        """Base queryset for the view. Filtering/search handled by backends.

        We keep this method to return the base QuerySet and to preserve a
        consistent return type for static checkers.
        """
        return Book.objects.all()


class BookDetailView(generics.RetrieveAPIView):
    """Retrieve a single book by ID (pk)."""

    permission_classes = [permissions.AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(generics.CreateAPIView):
    """Create a new book."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class BookUpdateView(generics.UpdateAPIView):
    """Update an existing book."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_update(serializer)
        return Response(serializer.data)


class BookDeleteView(generics.DestroyAPIView):
    """Delete a book."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
