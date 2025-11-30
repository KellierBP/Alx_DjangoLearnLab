from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


"""
Serializers for the API app.

BookSerializer: serializes all fields of the Book model and includes
custom validation to ensure `publication_year` is not in the future.

AuthorSerializer: includes the `name` field and a nested list of books
using `BookSerializer`. The nested `books` field is populated from the
Author -> Book relation (related_name='books'). The nested representation
is read-only by default here; writes could be implemented with
custom create/update methods if nested writes are needed.
"""


class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model.

    Includes a validation method to prevent setting a publication year
    in the future.
    """

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """Ensure the publication_year is not in the future."""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("publication_year cannot be in the future")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for the Author model.

    The `books` field uses the nested `BookSerializer` to present the
    author's related Book instances. Because Book has `related_name='books'`,
    the serializer can access `author.books.all()` automatically.
    """

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
