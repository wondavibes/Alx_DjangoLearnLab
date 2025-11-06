from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Author, Book
from .models import Library, Librarian


def list_books(request):
    """Display a list of all books and their authors using a template."""
    books = Book.objects.all().select_related("author")
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    """Display details of a specific library and its books."""

    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_queryset(self):
        """Optimize the query by prefetching related books and their authors."""
        return Library.objects.prefetch_related(
            "books", "books__author"
        ).select_related("librarian")
