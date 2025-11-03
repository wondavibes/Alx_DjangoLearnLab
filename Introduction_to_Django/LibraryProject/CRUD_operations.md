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

# update.md

# Open Django shell
python manage.py shell

# Import the Book model
from your_app.models import Book

# Retrieve and update the book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Confirm update
print(book.title)
# Expected output: Nineteen Eighty-Four

# delete.md

# Open Django shell
python manage.py shell

# Import the Book model
from your_app.models import Book

# Retrieve and delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion
print(Book.objects.all())
# Expected output: <QuerySet []> — confirms no books exist