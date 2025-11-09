# Admin Fieldsets Configuration

## Overview
The `fieldsets` option organizes fields in the admin change form (the detailed edit page) into logical sections. This improves the user experience by grouping related information together.

## Configuration

### Code Implementation
```python
class BookAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'publication_year')
        }),
    )
```

## What Gets Displayed

When you edit a book in the admin, the form displays all fields grouped under the section "Book Information".

### Example Change Form
```
Book Information
═══════════════════════════════════════════
Title:              [Text Input Field]
Author:             [Text Input Field]
Publication Year:   [Number Input Field]
```

## Fieldsets Structure

A fieldset is a tuple containing:
1. **Section Title** (string): The name of the section displayed as a heading
2. **Configuration Dictionary**: Contains field options

### Configuration Dictionary Keys

| Key | Description | Required |
|-----|-------------|----------|
| `fields` | Tuple of field names to display | Yes |
| `classes` | CSS classes for styling (e.g., 'collapse', 'wide') | No |
| `description` | Help text displayed above the fieldset | No |

## Fieldsets Examples

### Basic Single Fieldset
```python
fieldsets = (
    ('Book Information', {
        'fields': ('title', 'author', 'publication_year')
    }),
)
```

### Multiple Fieldsets
```python
fieldsets = (
    ('Basic Information', {
        'fields': ('title', 'author')
    }),
    ('Publication Details', {
        'fields': ('publication_year',),
        'description': 'Information about when the book was published'
    }),
)
```

### With CSS Classes
```python
fieldsets = (
    ('Book Information', {
        'fields': ('title', 'author', 'publication_year'),
        'classes': ('wide',),
    }),
    ('Advanced Options', {
        'fields': ('status',),
        'classes': ('collapse',),  # Creates collapsible section
        'description': 'Optional advanced settings'
    }),
)
```

## CSS Classes

### Available Classes

| Class | Effect |
|-------|--------|
| `wide` | Makes fields span full width |
| `collapse` | Creates a collapsible fieldset (collapsed by default) |
| `extrapretty` | Adds special styling |

### Usage Example
```python
fieldsets = (
    ('Main Information', {
        'fields': ('title', 'author'),
        'classes': ('wide',)
    }),
    ('Optional Details', {
        'fields': ('publication_year',),
        'classes': ('collapse',)
    }),
)
```

## Field Layout Options

### Single Column Layout
```python
'fields': ('title', 'author', 'publication_year')
# Displays as vertical stack
```

### Multi-Column Layout
```python
'fields': (
    ('title', 'author'),  # Two columns on one row
    ('publication_year',),  # One column on next row
)
```

## Real-World Example

```python
class BookAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Book Details', {
            'fields': (('title', 'author'), 'publication_year'),
            'description': 'Enter the book title and author information',
            'classes': ('wide',)
        }),
        ('Publication Info', {
            'fields': ('publication_year', 'isbn'),
            'classes': ('collapse',),
        }),
    )
```

## Benefits

✅ Improved form organization
✅ Better user experience for complex models
✅ Logical grouping of related fields
✅ Reduces clutter and confusion
✅ Professional-looking admin interface
✅ Collapsible sections save screen space

## When to Use Fieldsets

**Use fieldsets when:**
- Model has many fields (more than 5-10)
- Fields can be logically grouped
- Want to improve admin usability
- Need to hide advanced options by default

**Don't use fieldsets when:**
- Model has only 2-3 fields
- All fields are equally important
- Form is already simple and organized
