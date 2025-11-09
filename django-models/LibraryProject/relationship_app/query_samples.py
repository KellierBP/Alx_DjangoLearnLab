import django
import os

# Setup Django environment (only if running this file standalone)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def sample_queries():
    # 1️⃣ Query all books by a specific author
    author_name = "J.K. Rowling"
    try:
        author = Author.objects.get(name=author_name)
        books_by_author = Book.objects.filter(author=author)
        print(f"Books by {author_name}:")
        for book in books_by_author:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"No author found with name '{author_name}'")

    # 2️⃣ List all books in a library
    library_name = "Central Library"
    try:
        library = Library.objects.get(name=library_name)
        books_in_library = library.books.all()
        print(f"\nBooks in {library_name}:")
        for book in books_in_library:
            print(f"- {book.title} by {book.author.name}")
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'")

    # 3️⃣ Retrieve the librarian for a library using Librarian.objects.get
    try:
        librarian = Librarian.objects.get(library=library)
        print(f"\nLibrarian for {library_name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to '{library_name}'")


if __name__ == "__main__":
    sample_queries()
