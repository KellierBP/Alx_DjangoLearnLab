# RETRIEVE Operation

## Description
Retrieve and display all attributes of the book created with title "1984".

## Python Command
```python
from bookshelf.models import Book
book = Book.objects.get(title='1984')
print(f'Title: {book.title}')
print(f'Author: {book.author}')
print(f'Publication Year: {book.publication_year}')
print(f'Book ID: {book.id}')
```

## Expected Output
```
Title: 1984
Author: George Orwell
Publication Year: 1949
Book ID: 1
```

## Explanation
- The `Book.objects.get()` method retrieves a single book record from the database using the specified query parameter (title='1984').
- The retrieved book object contains all the attributes that were previously stored:
  - **id**: Auto-generated primary key (1 for the first record)
  - **title**: "1984"
  - **author**: "George Orwell"
  - **publication_year**: 1949
- All attributes are displayed to confirm successful retrieval from the database.
