# UPDATE Operation

## Description
Update the title of the book from "1984" to "Nineteen Eighty-Four" and save the changes.

## Python Command
```python
from bookshelf.models import Book
book = Book.objects.get(title='1984')
book.title = 'Nineteen Eighty-Four'
book.save()
print(f'Updated title: {book.title}')
```

## Expected Output
```
Updated title: Nineteen Eighty-Four
```

## Explanation
- The `Book.objects.get()` method retrieves the book record by its current title.
- The `title` attribute is modified with the new value: "Nineteen Eighty-Four"
- The `save()` method persists the changes to the database.
- After the update, the book's title is confirmed to be "Nineteen Eighty-Four"
- The book ID and other attributes remain unchanged.
