# Django Admin Configuration - Quick Reference

## Configuration Overview

```python
from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author')
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'publication_year')
        }),
    )

admin.site.register(Book, BookAdmin)
```

---

## Features at a Glance

### 📋 List Display
**What**: Shows books in a table format
**Config**: `list_display = ('title', 'author', 'publication_year')`
**Result**: 3 sortable columns displaying book information

### 🔍 Search
**What**: Find books quickly
**Config**: `search_fields = ('title', 'author')`
**Usage**: Type in search box at top
**Example**: Search "1984" → finds book titled "1984"

### 🎯 Filters
**What**: Narrow down book list
**Config**: `list_filter = ('publication_year', 'author')`
**Usage**: Click filters in right sidebar
**Example**: Click "1949" → shows only 1949 books

### 📝 Form Organization
**What**: Organize edit form fields
**Config**: `fieldsets = (('Book Information', {...}),)`
**Result**: Form grouped into sections with headers

---

## Quick Commands

### Access Admin
```bash
# Start server
python manage.py runserver

# Open admin (in browser)
http://localhost:8000/admin/

# Create superuser (if needed)
python manage.py createsuperuser
```

---

## Admin Operations

| Operation | Steps |
|-----------|-------|
| **Add Book** | Click "Add Book" → Fill form → Save |
| **Edit Book** | Click book title → Modify → Save |
| **Delete Book** | Click book title → Delete → Confirm |
| **Search** | Type in search box → Press Enter |
| **Filter** | Click filter in sidebar → View results |
| **Sort** | Click column header → Arrow shows direction |
| **Combine Filters** | Click year + author filter → See results |

---

## Field Reference

### Available for Search
- `title` - Book title
- `author` - Author name

### Available for Filter
- `publication_year` - Year book published
- `author` - Author name

### Displayed in List
- `title` - Book title (sortable)
- `author` - Author name (sortable)
- `publication_year` - Publication year (sortable)

---

## Common Configuration Options

```python
# Show specific fields in list view
list_display = ('title', 'author', 'publication_year')

# Add filter options (sidebar)
list_filter = ('publication_year', 'author')

# Add search capability
search_fields = ('title', 'author')

# Organize form layout
fieldsets = (
    ('Book Information', {'fields': ('title', 'author', 'publication_year')}),
)

# Set default sort order
ordering = ('title',)

# Items per page
list_per_page = 25

# Make fields read-only
readonly_fields = ('id', 'created_at')

# Make fields inline editable
list_editable = ('author',)
```

---

## Troubleshooting Quick Tips

| Problem | Fix |
|---------|-----|
| No Book model in admin | Check admin.site.register() call |
| Search not working | Verify search_fields field names |
| Filters missing | Verify list_filter field names |
| Can't login | Create superuser: `python manage.py createsuperuser` |
| Admin won't load | Add 'bookshelf' to INSTALLED_APPS in settings.py |

---

## Important Notes

✅ Always register model with `admin.site.register()`
✅ Use descriptive field names
✅ Keep search fields limited to frequently searched columns
✅ Choose filters with limited unique values
✅ Test after any configuration changes
✅ Restart server after modifying admin.py

---

## Documentation Files

- **ADMIN_CONFIGURATION.md** - Complete detailed guide
- **ADMIN_USER_GUIDE.md** - How to use admin interface
- **admin_registration.md** - Model registration details
- **admin_list_display.md** - List display customization
- **admin_list_filter.md** - Filter setup and usage
- **admin_search.md** - Search functionality guide
- **admin_fieldsets.md** - Form organization

---

## File Location

📁 `bookshelf/admin.py` - Main configuration file
📁 `bookshelf/models.py` - Book model definition
🔧 `LibraryProject/settings.py` - App registration

---

## Status: ✅ COMPLETE

All admin configurations implemented and documented.
Ready for production use.
