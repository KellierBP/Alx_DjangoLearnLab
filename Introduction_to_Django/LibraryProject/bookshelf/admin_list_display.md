# Admin List Display Customization

## Overview
The `list_display` option controls which fields appear in the admin list view (the main admin page for a model).

## Configuration

### Code Implementation
```python
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
```

## What Gets Displayed

When you visit the Book admin list page, you will see:
- **Column 1**: Title (book title)
- **Column 2**: Author (author name)
- **Column 3**: Publication Year (year the book was published)

### Example Display
```
Title                      Author              Publication Year
================================================
1984                       George Orwell       1949
To Kill a Mockingbird      Harper Lee          1960
The Great Gatsby           F. Scott Fitzgerald 1925
```

## Features Enabled

### 1. Sortable Columns
- Click on any column header to sort by that field
- Click again to reverse the sort order
- Indicated by up/down arrows next to the column name

### 2. Row Selection
- Checkbox next to each row for bulk operations
- Select multiple books to perform actions on them

### 3. Click to Edit
- Click on any field value to open the detailed edit page
- Allows you to modify the book's information

## Best Practices

1. **Include Primary Information**: Always include fields that help identify the record (like title)
2. **Limit Columns**: Don't display too many columns (typically 3-5) to keep the interface clean
3. **Readable Field Names**: Django automatically converts field names to readable titles (publication_year becomes "Publication Year")
4. **Related Fields**: Can include related model fields using double underscores (e.g., 'author__name')

## Advanced Options

### Make Fields Clickable
```python
list_display_links = ('title',)  # Click on title to edit
```

### Add Custom Methods
```python
def book_age(self, obj):
    from datetime import datetime
    return datetime.now().year - obj.publication_year
book_age.short_description = 'Years Since Publication'
list_display = ('title', 'author', 'publication_year', 'book_age')
```
