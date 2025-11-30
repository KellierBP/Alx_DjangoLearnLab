from django.db import models


"""
Models for the API app.

Author: stores a simple author name.
Book: stores title, publication year and a ForeignKey to Author.

The relationship is one-to-many: an Author can have many Book instances.
We use `related_name='books'` on the ForeignKey so the author's related
books can be accessed via `author.books.all()` which is convenient when
serializing nested relationships.
"""


class Author(models.Model):
	"""Represents an author.

	Fields
	- name: the author's full name (string)
	"""

	name = models.CharField(max_length=255)

	def __str__(self) -> str:  # pragma: no cover - simple repr
		return self.name


class Book(models.Model):
	"""Represents a book written by an author.

	Fields
	- title: the book's title
	- publication_year: 4-digit year the book was published
	- author: ForeignKey to `Author`, establishing one-to-many relation
	"""

	title = models.CharField(max_length=255)
	publication_year = models.IntegerField()
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

	def __str__(self) -> str:  # pragma: no cover - simple repr
		return f"{self.title} ({self.publication_year})"

