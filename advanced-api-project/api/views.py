from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
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

    def get_queryset(self) -> QuerySet[Book]:  # type: ignore[override]
        """Support simple filtering by author (id or name) and publication year via query params.

        Examples:
        - /api/books/?author=George
        - /api/books/?author=3
        - /api/books/?publication_year=1999
        """
        qs = Book.objects.all()
        params = cast(DRFRequest, self.request).query_params
        author = params.get("author")
        year = params.get("publication_year") or params.get("year")
        if author:
            if author.isdigit():
                qs = qs.filter(author_id=int(author))
            else:
                qs = qs.filter(author__name__icontains=author)
        if year and year.isdigit():
            qs = qs.filter(publication_year=int(year))
        return qs


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
