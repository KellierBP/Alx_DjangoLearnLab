API app - Book views
======================

This README documents the generic DRF views implemented in the `api` app
for the `Book` model.

Views and endpoints
- `BookList` (`GET /api/books/`): returns a list of books. Optional
  query parameter `author` filters by author id (e.g. `/api/books/?author=2`).
- `BookCreate` (`POST /api/books/create/`): creates a new `Book`.
  Requires authentication.
- `BookDetail` (`GET /api/books/<pk>/`): retrieves a single book.
- `BookUpdate` (`PUT/PATCH /api/books/<pk>/update/`): updates a book.
  Requires authentication.
- `BookDelete` (`DELETE /api/books/<pk>/delete/`): deletes a book.
  Requires authentication.

Permissions
- List and Detail: read-only access for all users (`AllowAny`).
- Create/Update/Delete: restricted to authenticated users (`IsAuthenticated`).

Serializer behavior
- `BookSerializer` (in `serializers.py`) performs validation to ensure
  `publication_year` is not in the future. Create/Update views rely on the
  serializer for validation.

Testing examples (curl)
- List books (public):

```bash
curl -s -X GET http://127.0.0.1:8000/api/books/ | jq
```

- Create book (authenticated):

```bash
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{"title":"New Book","publication_year":2020,"author":1}'
```

- Update book (authenticated):

```bash
curl -X PATCH http://127.0.0.1:8000/api/books/3/update/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{"title":"Updated Title"}'
```

- Delete book (authenticated):

```bash
curl -X DELETE http://127.0.0.1:8000/api/books/3/delete/ -u username:password
```

Notes and extension points
- If you want to attach the creating user to a Book, add an `owner` field
  to the `Book` model and call `serializer.save(owner=self.request.user)` in
  `BookCreate.perform_create`.
- For richer filtering/searching, enable DRF filters in `settings.py`
  (`DEFAULT_FILTER_BACKENDS`) and add `filter_backends` / `filterset_fields`
  to `BookList`.
