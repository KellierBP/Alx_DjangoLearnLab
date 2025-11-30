from django.contrib import admin
from .models import Author, Book


"""Admin registration for API models to allow manual testing via Django admin."""


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'publication_year', 'author')

