import datetime
from rest_framework import serializers
from .models import Book, Author


class BookSerializer(serializers.ModelSerializer):
    # Represent the Book's author using the author's 'name' (SlugRelatedField).
    # This is read-only to avoid attempting to create/modify Author objects when
    # creating/updating Books via this serializer. Using a simple scalar field
    # (author name) here also prevents infinite recursion when Book is nested
    # inside AuthorSerializer.
    author = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Book
        fields = "__all__"

    def validate_publication_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                "publication_year cannot be in the future."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
     books = BookSerializer(many=True, read_only=True)
    # Nested representation of an Author's books.
    # - `books` uses the BookSerializer to dynamically serialize all related Book instances.
    # - `many=True` because an Author can have multiple Book objects.
    # - `read_only=True` means Books are displayed but not created/updated via this field.
    # - `source="books"` assumes the Book model's ForeignKey to Author uses
    #   related_name="books". If the ForeignKey uses the default related_name,
   

    class Meta:
        model = Author
        fields = ["name", "books"]
