# delete.md

# Open Django shell
python manage.py shell

# Import the Book model
from bookshelf.models import Book

# Retrieve and delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

🚀