# CREATE Operation

## Description
Create a new Book instance with specific attributes.

## Python Command
```python
from bookshelf.models import Book
book = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)
print(book)
```

## Expected Output
```
1984
```

## Explanation
- The `Book.objects.create()` method instantiates and saves a new Book record to the database in a single operation.
- The book is created with:
  - **title**: "1984"
  - **author**: "George Orwell"
  - **publication_year**: 1949
- The `__str__` method of the Book model returns the title, so printing the book displays "1984"
- The book is immediately persisted to the database with an auto-generated ID.
