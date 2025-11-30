"""URL routes for the `api` app.

This module exposes endpoints for the Book generic views implemented
in `api.views`.

Endpoints:
- `books/`                 : GET list of books
- `books/create/`          : POST create a new book
- `books/<int:pk>/`        : GET retrieve a single book
- `books/<int:pk>/update/` : PUT/PATCH update a book
- `books/<int:pk>/delete/` : DELETE remove a book
"""

from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('books/', views.BookList.as_view(), name='book-list'),
    path('books/create/', views.BookCreate.as_view(), name='book-create'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
    # Endpoints that accept an `id` in the request body/query params
    # These provide routes matching `books/update` and `books/delete`.
    path('books/update', views.BookUpdateNoPK.as_view(), name='book-update-no-pk'),
    path('books/delete', views.BookDeleteNoPK.as_view(), name='book-delete-no-pk'),
]
