# DELETE Operation

## Description
Delete the book instance and confirm the deletion by attempting to retrieve all books.

## Python Command
```python
from bookshelf.models import Book
book = Book.objects.get(title='Nineteen Eighty-Four')
book.delete()
# Confirm deletion
remaining_books = Book.objects.all()
print(f'Books remaining: {len(remaining_books)}')
```

## Expected Output
```
Books remaining: 0
```

## Explanation
- The `Book.objects.get()` method retrieves the book with the updated title "Nineteen Eighty-Four".
- The `delete()` method removes the book record from the database.
- After deletion, `Book.objects.all()` is called to retrieve all books in the database.
- The result shows 0 books remaining, confirming that the deletion was successful.
- The database is now empty with no Book records.
