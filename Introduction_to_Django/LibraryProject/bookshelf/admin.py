from django.contrib import admin
from .models import Book


class BookAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters for easier filtering
    list_filter = ('publication_year', 'author')
    
    # Add search functionality
    search_fields = ('title', 'author')
    
    # Organize fields in the change form
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'publication_year')
        }),
    )


# Register the Book model with the custom admin
admin.site.register(Book, BookAdmin)
