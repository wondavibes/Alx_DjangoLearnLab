# retrieve.md

# Open Django shell
python manage.py shell

# Import the Book model
from your_app.models import Book

# Retrieve the book
book = Book.objects.get(title="1984")

# Display all attributes
print(book.title, book.author, book.publication_year)
# Expected output: 1984 George Orwell 1949
