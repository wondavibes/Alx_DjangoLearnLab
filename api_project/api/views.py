from django.shortcuts import render
from rest_framework import generics
from .models import Book

# Create your views here.
from .serializers import BookSerializer


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
