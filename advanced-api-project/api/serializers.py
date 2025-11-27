import datetime
from rest_framework import serializers
from .models import Book, Author


class BookSerializer(serializers.ModelSerializer):
    # Use a writable SlugRelatedField for `author` so the API can accept the
    # author's name on write operations while still representing the author by
    # name on reads. The `queryset` argument makes the field writable and
    # instructs DRF how to resolve the provided slug value to an Author.
    author = serializers.SlugRelatedField(
        slug_field="name", queryset=Author.objects.all()
    )

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
