from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from .models import Author, Book
from .models import Library, Librarian, CustomUser
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.urls import reverse_lazy, reverse
from .forms import BookForm, CustomUserCreationForm  # You'll need to create this form
from django.contrib.auth.views import LoginView as AuthLoginView


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
    """Handle user registration with a custom user creation form."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")
    else:
        form = CustomUserCreationForm()
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


class CustomLoginView(AuthLoginView):
    """
    Respects ?next= first (inherited behavior). If no next, redirect by user role.
    """

    def get_success_url(self) -> str:
        # Respect ?next= parameter
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to

        # Access role directly from the custom user model
        user = self.request.user
        role = getattr(user, "role", None)

        if role == "Admin":
            return reverse("admin_view")
        elif role == "Librarian":
            return reverse("librarian_view")
        elif role == "Member":
            return reverse("member_view")
        else:
            return reverse("list_books")


def home(request):
    """
    Simple homepage that offers role-specific login links (uses ?next= to direct after login).
    """
    return render(request, "relationship_app/home.html")
