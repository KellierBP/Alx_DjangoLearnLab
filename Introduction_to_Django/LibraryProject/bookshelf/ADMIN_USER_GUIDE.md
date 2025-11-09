# Django Admin User Guide - Practical Usage

## Getting Started with Django Admin

### Step 1: Start the Development Server
```bash
cd c:\Users\user\Desktop\Alx_DjangoLearnLab\Introduction_to_Django\LibraryProject
python manage.py runserver
```

**Output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 2: Access the Admin Interface
Open your web browser and go to:
```
http://localhost:8000/admin/
```

### Step 3: Login
- **Username**: Your superuser username
- **Password**: Your superuser password

**Note**: If you haven't created a superuser, run:
```bash
python manage.py createsuperuser
```

---

## Admin Dashboard Overview

### Main Admin Page
```
DJANGO ADMINISTRATION

Welcome, [username]!

BOOKSHELF
├─ Books [Change] [Add]

AUTHENTICATION AND AUTHORIZATION
├─ Groups
├─ Users
```

Click on "Books" or "Add" to manage books.

---

## Adding a Book

### Steps

1. **Click "Add Book" Button**
   - Location: Admin dashboard, bookshelf section
   - Or navigate to: `http://localhost:8000/admin/bookshelf/book/add/`

2. **Fill in the Form**
   ```
   Book Information
   ──────────────────────────────────
   Title:              [1984]
   Author:             [George Orwell]
   Publication Year:   [1949]
   ```

3. **Save the Book**
   - Click "Save" button → Redirects to list view
   - Click "Save and Continue Editing" → Stays on edit form
   - Click "Save and Add Another" → Opens new form immediately

### Example: Add "To Kill a Mockingbird"
```
Title:              To Kill a Mockingbird
Author:             Harper Lee
Publication Year:   1960
[Save]
```

**Result**: "To Kill a Mockingbird" appears in the book list.

---

## Viewing and Editing Books

### View All Books
- Navigate to admin list view: `http://localhost:8000/admin/bookshelf/book/`
- Shows all books in a table format

### Table View
```
Title                      Author                 Publication Year
════════════════════════════════════════════════════════════════
[☐] 1984                   George Orwell          1949
[☐] To Kill a Mockingbird  Harper Lee             1960
[☐] The Great Gatsby       F. Scott Fitzgerald    1925
```

### Edit a Book
1. Click on the book title (e.g., "1984")
2. Modify any field
3. Click "Save"

### Change Example
**Before:**
```
Title: 1984
Author: George Orwell
Publication Year: 1949
```

**After:**
```
Title: Nineteen Eighty-Four
Author: George Orwell
Publication Year: 1949
[Save]
```

**Result**: Title is updated to "Nineteen Eighty-Four"

---

## Searching for Books

### Using the Search Box
1. Locate the search box at the top of the book list
2. Type your search query
3. Press Enter or results update automatically

### Search Examples

**Search by Title**
- Input: "1984"
- Result: Shows "1984", "1984 Annotated Edition", etc.

**Search by Author**
- Input: "orwell"
- Result: Shows all books by George Orwell

**Partial Search**
- Input: "great"
- Result: Shows "The Great Gatsby" and any book with "great" in title/author

**No Results**
- Input: "unknown author"
- Result: Empty list with message "0 books"

---

## Filtering Books

### Available Filters
In the right sidebar, you'll see:
```
FILTER
├─ Publication Year
│  ├─ 1925
│  ├─ 1949
│  ├─ 1960
│  └─ ...
├─ Author
│  ├─ F. Scott Fitzgerald
│  ├─ George Orwell
│  ├─ Harper Lee
│  └─ ...
└─ Clear all filters
```

### Filter by Publication Year
1. Click on a year (e.g., "1949")
2. List shows only books from that year
3. URL changes to include filter parameter

**Example**: Click "1949"
```
Result: Shows only "1984" by George Orwell
Title              Author          Publication Year
─────────────────────────────────────────────
1984               George Orwell   1949
```

### Filter by Author
1. Click on an author name (e.g., "George Orwell")
2. List shows only books by that author
3. URL updates to reflect filter

**Example**: Click "George Orwell"
```
Result: Shows all books by George Orwell
Title              Author          Publication Year
─────────────────────────────────────────────
1984               George Orwell   1949
```

### Combine Filters
1. First, click publication year "1949"
2. Then, click author "George Orwell"
3. Result shows intersection (books matching both criteria)

**Example**: Year="1949" AND Author="George Orwell"
```
Result: Shows "1984"
Title              Author          Publication Year
─────────────────────────────────────────────
1984               George Orwell   1949
```

### Clear Filters
- Click "Clear all filters" link
- List returns to showing all books

---

## Sorting Books

### Sort by Column Headers
- Click any column header to sort ascending
- Click again to sort descending
- Arrow indicator shows sort direction

### Sort Examples

**Sort by Title (A-Z)**
- Click "Title" header
- Books appear in alphabetical order

**Sort by Title (Z-A)**
- Click "Title" header again
- Books appear in reverse alphabetical order

**Sort by Publication Year (Oldest First)**
- Click "Publication Year" header
- Books ordered from 1920s to 2020s

**Sort by Publication Year (Newest First)**
- Click "Publication Year" header again
- Books ordered from 2020s to 1920s

---

## Deleting Books

### Delete Single Book
1. Click on the book title
2. Scroll to bottom of form
3. Click "Delete" button (red, at bottom)
4. Confirm deletion on next page
5. Book is removed from database

### Delete Multiple Books (Bulk Action)
1. Check boxes next to books you want to delete
2. Select "Delete selected books" from dropdown
3. Click "Go"
4. Confirm deletion

**Example**:
```
[☐] 1984
[☑] To Kill a Mockingbird
[☑] The Great Gatsby

Action: Delete selected books
[Go]

Result: "The Great Gatsby" and "To Kill a Mockingbird" are deleted
```

---

## Common Admin Tasks

### Task 1: Find and Edit a Book
**Goal**: Change "1984" to "Nineteen Eighty-Four"

**Steps**:
1. Search for "1984"
2. Click on the result
3. Change title to "Nineteen Eighty-Four"
4. Click "Save"

### Task 2: Find All Books by an Author
**Goal**: See all books by George Orwell

**Steps**:
1. Click filter "George Orwell" under Author
2. View all Orwell books

### Task 3: Find All Books from a Specific Year
**Goal**: See all books published in 1949

**Steps**:
1. Click filter "1949" under Publication Year
2. View all 1949 books

### Task 4: Add Multiple Books
**Goal**: Add 3 new books

**Steps**:
1. Click "Add Book"
2. Fill in form for Book 1
3. Click "Save and Add Another"
4. Fill in form for Book 2
5. Click "Save and Add Another"
6. Fill in form for Book 3
7. Click "Save"

### Task 5: Export Book Data
**Goal**: See all book information at once

**Steps**:
1. Go to book list
2. Use browser DevTools or external tools to export
3. Or copy/paste data as needed

---

## Tips and Tricks

### 1. Keyboard Shortcuts
- `Tab` - Navigate between form fields
- `Enter` - Submit form (sometimes)
- `Escape` - Close modals/dialogs

### 2. Search Tips
- Search is case-insensitive
- Partial matches work: "orw" finds "Orwell"
- Both title and author are searched simultaneously

### 3. Filter Tips
- Filters are cumulative (AND logic)
- Click filter again to remove it
- "Clear all filters" removes all active filters

### 4. Sorting Tips
- Sortable columns have different cursor appearance
- Current sort shown by arrow (↑ or ↓)
- Sort persists when using filters/search

### 5. Edit Tips
- Click any field name to directly edit it
- Use Tab to move between fields
- Form auto-saves after you click Save

### 6. Navigation Tips
- Use browser back button to return to list
- Breadcrumb navigation at top shows path
- Home button returns to admin dashboard

---

## Admin Interface Features Summary

| Feature | Location | Purpose |
|---------|----------|---------|
| Search Box | Top of list | Find books by title or author |
| Filters | Right sidebar | Filter books by year or author |
| Sort | Column headers | Arrange books in desired order |
| Add Button | Top right | Create new book |
| Edit | Click title | Modify book details |
| Delete | Book detail page | Remove book from database |
| Checkboxes | Left of each row | Select multiple books |
| Actions | Below list | Perform bulk operations |

---

## Troubleshooting

### Problem: Can't Login
- **Check**: Username and password are correct
- **Check**: Superuser account exists
- **Solution**: Create superuser with `python manage.py createsuperuser`

### Problem: Book Model Not Appearing
- **Check**: Bookshelf app is in INSTALLED_APPS
- **Check**: Model is registered in admin.py
- **Solution**: Restart development server

### Problem: Filters Not Working
- **Check**: Field names in list_filter are correct
- **Solution**: Check admin.py list_filter configuration

### Problem: Search Not Working
- **Check**: Field names in search_fields are correct
- **Solution**: Restart development server, check admin.py

### Problem: Can't Edit/Delete Books
- **Check**: You have appropriate permissions
- **Solution**: Request permissions from admin or superuser

---

## Best Practices

1. **Always use search first** - Faster than browsing
2. **Use filters to narrow** - Then search within results
3. **Keep titles descriptive** - Easy to identify books
4. **Regular backups** - Don't lose important data
5. **Test before production** - Verify changes work

---

## Additional Resources

- **Django Admin Documentation**: https://docs.djangoproject.com/en/stable/ref/contrib/admin/
- **Django Models**: https://docs.djangoproject.com/en/stable/topics/db/models/
- **Django ORM**: https://docs.djangoproject.com/en/stable/topics/db/
