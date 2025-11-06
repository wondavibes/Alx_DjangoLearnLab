# update.md

# Open Django shell
python manage.py shell

# Import the Book model
from  bookshelf.models import Book

# Retrieve and update the book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Confirm update
print(book.title)
# Expected output: Nineteen Eighty-Four