from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Author, Book
from .models import Library, Librarian
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import BookForm  # You'll need to create this form


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

    return render(request, "relationship_app/register.html", {"form": form})


def has_role(user, role_name):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == role_name
    )


@user_passes_test(lambda u: has_role(u, "Admin"))
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(lambda u: has_role(u, "Librarian"))
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(lambda u: has_role(u, "Member"))
def member_view(request):
    return render(request, "relationship_app/member_view.html")


@permission_required("relationship_app.can_add_book")
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm()
    return render(request, "relationship_app/book_form.html", {"form": form})


@permission_required("relationship_app.can_change_book")
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm(instance=book)
    return render(request, "relationship_app/book_form.html", {"form": form})


@permission_required("relationship_app.can_delete_book")
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    return render(request, "relationship_app/book_confirm_delete.html", {"book": book})


# Alternative: Class-based views with permissions
"""class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "relationship_app/book_form.html"
    success_url = reverse_lazy("list_books")
    permission_required = "relationship_app.can_add_book"


class BookUpdateView(PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "relationship_app/book_form.html"
    success_url = reverse_lazy("list_books")
    permission_required = "relationship_app.can_change_book"


class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = "relationship_app/book_confirm_delete.html"
    success_url = reverse_lazy("list_books")
    permission_required = "relationship_app.can_delete_book"
"""
