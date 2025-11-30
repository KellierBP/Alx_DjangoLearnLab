"""API views for the `api` application.

This module implements DRF generic views to handle CRUD operations for the
`Book` model. The goal is to show how to use DRF generic views and
permission classes to provide secure, concise endpoints.

Views provided:
- `BookList`    : GET list of books (public)
- `BookDetail`  : GET single book by `pk` (public)
- `BookCreate`  : POST create a book (authenticated only)
- `BookUpdate`  : PUT/PATCH update a book (authenticated only)
- `BookDelete`  : DELETE a book (authenticated only)

The Create/Update views perform standard serializer validation (the
`BookSerializer` already enforces `publication_year` not being in the
future). The list view supports optional filtering by `author` via a
query parameter (e.g. `?author=3`).
"""

from rest_framework import generics, permissions

from .models import Book
from .serializers import BookSerializer


class BookList(generics.ListAPIView):
	"""List all books. Publicly readable.

	Optional query params:
	- `author`: integer author id to filter books by author
	"""

	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]

	def get_queryset(self):
		queryset = super().get_queryset()
		author_id = self.request.query_params.get('author')
		if author_id:
			queryset = queryset.filter(author_id=author_id)
		return queryset


class BookDetail(generics.RetrieveAPIView):
	"""Retrieve a single book by primary key. Publicly readable."""

	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]


class BookCreate(generics.CreateAPIView):
	"""Create a new book. Only authenticated users may create."""

	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		# No extra fields to set on save currently, but method kept
		# to show where additional logic (e.g. attaching request.user)
		# would go.
		serializer.save()


class BookUpdate(generics.UpdateAPIView):
	"""Update an existing book. Only authenticated users may update."""

	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_update(self, serializer):
		serializer.save()


class BookDelete(generics.DestroyAPIView):
	"""Delete a book. Only authenticated users may delete."""

	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]


# Backwards-compatible / alternate names
# Some tools or tests expect generic names such as `ListView`, `DetailView`,
# `CreateView`, `UpdateView`, and `DeleteView`. Provide simple aliases that
# point to the implementations above so both naming styles work.
ListView = BookList
DetailView = BookDetail
CreateView = BookCreate
UpdateView = BookUpdate
DeleteView = BookDelete

