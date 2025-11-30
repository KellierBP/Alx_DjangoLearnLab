from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authenticated actions
        self.user = User.objects.create_user(username='tester', password='password')

        # Create authors
        self.author1 = Author.objects.create(name='Author One')
        self.author2 = Author.objects.create(name='J.R.R. Tolkien')

        # Create books with varying titles and years
        self.book1 = Book.objects.create(title='A Tale', publication_year=1999, author=self.author1)
        self.book2 = Book.objects.create(title='The Ring', publication_year=1954, author=self.author2)
        self.book3 = Book.objects.create(title='Another Story', publication_year=2001, author=self.author1)

        self.list_url = reverse('api:book-list')
        self.create_url = reverse('api:book-create')

        self.client = APIClient()

    def test_list_books_default_ordering(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data
        # Ensure we returned the expected number
        self.assertEqual(len(results), 3)
        # Default ordering is by title (ascending)
        titles = [item['title'] for item in results]
        self.assertEqual(titles, sorted(titles))

    def test_filter_by_author(self):
        response = self.client.get(self.list_url, {'author': self.author1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data
        self.assertTrue(all(item['author'] == self.author1.id for item in results))

    def test_search_by_title_and_author(self):
        # Search by part of the title
        response = self.client.get(self.list_url, {'search': 'Ring'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'The Ring')

        # Search by author name
        response2 = self.client.get(self.list_url, {'search': 'Tolkien'})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        results2 = response2.data
        self.assertGreaterEqual(len(results2), 1)
        self.assertTrue(any('Tolkien' in self.author2.name for _ in results2))

    def test_ordering_by_publication_year(self):
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data
        years = [item['publication_year'] for item in results]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_create_requires_authentication(self):
        payload = {'title': 'New Book', 'publication_year': 2020, 'author': self.author1.id}
        response = self.client.post(self.create_url, payload, format='json')
        # Should be unauthorized (401) or forbidden (403) depending on auth settings
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        payload = {'title': 'New Book', 'publication_year': 2020, 'author': self.author1.id}
        response = self.client.post(self.create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        self.assertEqual(data['title'], 'New Book')
        self.assertEqual(data['publication_year'], 2020)

    def test_update_book_authenticated(self):
        url = reverse('api:book-update', kwargs={'pk': self.book1.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {'title': 'A Tale Updated'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'A Tale Updated')

    def test_delete_book_authenticated(self):
        url = reverse('api:book-delete', kwargs={'pk': self.book2.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book2.pk)
