from typing import Union, Optional

from django.core.exceptions import ObjectDoesNotExist

from relationship_app.models import Author, Book, Library, Librarian


def books_by_author(author: Union[int, str, Author]):
    """Return a QuerySet of books written by the provided author.

    Args:
        author: either an Author instance, an integer primary key, or the author's name (str).

    Returns:
        Django QuerySet of `Book` objects.

    Examples:
        books = books_by_author(1)
        books = books_by_author('Jane Austen')
        author = Author.objects.get(name='Jane Austen')
        books = books_by_author(author)
    """
    if isinstance(author, Author):
        return Book.objects.filter(author=author)
    if isinstance(author, int):
        return Book.objects.filter(author_id=author)
    if isinstance(author, str):
        return Book.objects.filter(author__name=author)
    raise ValueError("author must be an Author, int (pk), or str (name)")


def all_books_in_library(library: Union[int, str, Library]):
    """Return a QuerySet of all books in a given library.

    Args:
        library: Library instance, integer primary key, or library name (str).

    Returns:
        Django QuerySet of `Book` objects. If the Library is not found, returns an empty QuerySet.

    Examples:
        books = all_books_in_library(1)
        books = all_books_in_library('Central Library')
    """
    try:
        if isinstance(library, Library):
            lib = library
        elif isinstance(library, int):
            lib = Library.objects.get(pk=library)
        elif isinstance(library, str):
            lib = Library.objects.get(name=library)
        else:
            raise ValueError("library must be a Library, int (pk), or str (name)")
    except ObjectDoesNotExist:
        # Return empty queryset
        return Book.objects.none()

    # `books` is a ManyToMany on Library
    return lib.books.all()


def librarian_for_library(library: Union[int, str, Library]) -> Optional[Librarian]:
    """Return the Librarian for a given library.

    Args:
        library: Library instance, integer primary key, or library name (str).

    Returns:
        Librarian instance or None if not found.

    Examples:
        librarian = librarian_for_library(1)
        librarian = librarian_for_library('Central Library')
    """
    try:
        if isinstance(library, Library):
            lib = library
        elif isinstance(library, int):
            lib = Library.objects.get(pk=library)
        elif isinstance(library, str):
            lib = Library.objects.get(name=library)
        else:
            raise ValueError("library must be a Library, int (pk), or str (name)")
    except ObjectDoesNotExist:
        return None

    # OneToOne related name is `librarian` (see models)
    try:
        return lib.librarian  # type: ignore
    except ObjectDoesNotExist:
        return None


if __name__ == "__main__":
    # Example usage (requires Django environment configured)
    print(
        "Module `query_samples` loaded. Use the functions from a Django shell or view."
    )
