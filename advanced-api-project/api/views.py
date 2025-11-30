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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

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
 

class BookUpdateNoPK(APIView):
	"""Update a book when the client supplies `id` in the request body.

	This provides a `books/update` endpoint that accepts `PUT` or `PATCH`
	with JSON containing an `id` field and the fields to change. It is
	restricted to authenticated users.
	"""

	permission_classes = [permissions.IsAuthenticated]

	def _get_book(self, request):
		book_id = request.data.get('id') or request.query_params.get('id')
		if not book_id:
			return None, Response({'detail': 'Missing "id" in request.'}, status=status.HTTP_400_BAD_REQUEST)
		book = get_object_or_404(Book, pk=book_id)
		return book, None

	def put(self, request, *args, **kwargs):
		book, error = self._get_book(request)
		if error:
			return error
		serializer = BookSerializer(book, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)

	def patch(self, request, *args, **kwargs):
		book, error = self._get_book(request)
		if error:
			return error
		serializer = BookSerializer(book, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)


class BookDeleteNoPK(APIView):
	"""Delete a book when the client supplies `id` in the request body.

	Provides a `books/delete` endpoint that accepts `DELETE` and expects an
	`id` field in the request body or as a query parameter. Restricted to
	authenticated users.
	"""

	permission_classes = [permissions.IsAuthenticated]

	def delete(self, request, *args, **kwargs):
		book_id = request.data.get('id') or request.query_params.get('id')
		if not book_id:
			return Response({'detail': 'Missing "id" in request.'}, status=status.HTTP_400_BAD_REQUEST)
		book = get_object_or_404(Book, pk=book_id)
		book.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


