# CRUD operations with Django shell

Short reference: how to Create, Retrieve, Update and Delete `Book` instances using the Django shell.

## Prerequisites

- Your Django project is configured and migrated.
- The `Book` model exists in `bookshelf.models` (adjust import path if different).
- Run migrations if needed: `python manage.py migrate`.

## Table of contents

- [Create](#create)
- [Retrieve](#retrieve)
- [Update](#update)
- [Delete](#delete)
- [Notes & troubleshooting](#notes--troubleshooting)

---

## Create

Create a new `Book` instance from the Django shell.

Run the shell (bash):
```bash
python manage.py shell
```

Then in the Python shell:
```python
from bookshelf.models import Book   # adjust import if your app name differs

# create and save in one step
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949,
)

print(book)  # -> <Book: 1984>
```

Alternate (two-step) pattern:
```python
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()
```

---

## Retrieve

Get existing records.

Single item by unique field:
```python
from bookshelf.models import Book

book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)
# -> 1984 George Orwell 1949
```


---

## Update

Retrieve, modify, then save.

```python
from bookshelf.models import Book

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

print(book.title)  # -> Nineteen Eighty-Four
```

Bulk update example:
```python
Book.objects.filter(author="Unknown").update(author="Anonymous")
```

---

## Delete

Delete an instance or multiple records.

Single delete:
```python
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
```
---
