# CRUD Operations Documentation

## Overview
This document details all CRUD (Create, Read, Update, Delete) operations performed on the Book model in the bookshelf Django application.

---

## 1. CREATE Operation

### Command
```python
from bookshelf.models import Book
book = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)
print(book)
```

### Output
```
1984
```

### Explanation
The `create()` method instantiates and saves a new Book record in one operation. The book is created with:
- **title**: "1984"
- **author**: "George Orwell"
- **publication_year**: 1949

The `__str__` method returns the title, so the output displays "1984". The book is immediately saved to the database.

---

## 2. RETRIEVE Operation

### Command
```python
from bookshelf.models import Book
book = Book.objects.get(title='1984')
print(f'Title: {book.title}')
print(f'Author: {book.author}')
print(f'Publication Year: {book.publication_year}')
print(f'Book ID: {book.id}')
```

### Output
```
Title: 1984
Author: George Orwell
Publication Year: 1949
Book ID: 1
```

### Explanation
The `get()` method retrieves a single Book record from the database. All attributes of the created book are displayed:
- **id**: 1 (auto-generated primary key)
- **title**: "1984"
- **author**: "George Orwell"
- **publication_year**: 1949

---

## 3. UPDATE Operation

### Command
```python
from bookshelf.models import Book
book = Book.objects.get(title='1984')
book.title = 'Nineteen Eighty-Four'
book.save()
print(f'Updated title: {book.title}')
```

### Output
```
Updated title: Nineteen Eighty-Four
```

### Explanation
The UPDATE operation demonstrates:
1. Retrieving the book by its current title
2. Modifying the title attribute to "Nineteen Eighty-Four"
3. Calling `save()` to persist the changes to the database
4. Confirming the new title is saved

---

## 4. DELETE Operation

### Command
```python
from bookshelf.models import Book
book = Book.objects.get(title='Nineteen Eighty-Four')
book.delete()
# Confirm deletion
remaining_books = Book.objects.all()
print(f'Books remaining: {len(remaining_books)}')
```

### Output
```
Books remaining: 0
```

### Explanation
The DELETE operation demonstrates:
1. Retrieving the book with the updated title
2. Calling `delete()` to remove the record from the database
3. Verifying the deletion by querying all books
4. Confirming no books remain in the database

---

## Summary

The complete CRUD lifecycle for the Book model has been successfully demonstrated:
- **CREATE**: Book instance created with title="1984", author="George Orwell", publication_year=1949
- **RETRIEVE**: All book attributes successfully retrieved and displayed
- **UPDATE**: Book title successfully changed to "Nineteen Eighty-Four"
- **DELETE**: Book successfully deleted from the database

All operations were executed through the Django ORM, demonstrating proper usage of QuerySet methods and the model's interface.
