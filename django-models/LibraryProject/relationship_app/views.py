from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
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


def register(request):
    """Simple user registration view using Django's UserCreationForm.

    On successful registration, the new user is authenticated and logged in,
    then redirected to the book list page.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})
