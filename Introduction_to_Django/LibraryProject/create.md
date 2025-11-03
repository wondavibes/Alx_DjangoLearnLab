# create.md

# Open Django shell
python manage.py shell

# Import the Book model
from your_app.models import Book

# Create a Book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Output
print(book)
# Expected output: <Book: 1984> — confirms successful creation