# Alternative: Class-based views with permissions
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Book
from .forms import BookForm


class BookCreateView(PermissionRequiredMixin, CreateView):
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
