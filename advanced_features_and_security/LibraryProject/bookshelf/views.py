from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from .models import Book
from django.contrib.auth.decorators import permission_required, user_passes_test
from .forms import BookForm
from django import forms
from django.http import HttpResponse


def secure_view(request):
    response = HttpResponse("Secure content")
    response["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self' https://trusted.cdn.com"
    )
    return response


def book_list(request, book_id):
    """Display details of a single book."""
    book = get_object_or_404(Book, pk=book_id, raise_exception=True)
    return render(request, "bookshelf/book_detail.html", {"book": book})


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)


def search_books(request):
    form = SearchForm(request.GET)
    books = []
    if form.is_valid():
        query = form.cleaned_data["query"]
        books = Book.objects.filter(title__icontains=query)
    return render(
        request, "bookshelf/search_results.html", {"form": form, "books": books}
    )


# Create your views here.
@permission_required("bookshelf.can_create")
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm()
    return render(request, "bookshelf/book_form.html", {"form": form})


@permission_required("bookshelf.can_edit")
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/book_form.html", {"form": form})


@permission_required("bookshelf.can_delete")
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    return render(request, "bookshelf/book_confirm_delete.html", {"book": book})
