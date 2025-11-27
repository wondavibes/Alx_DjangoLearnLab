"""
Unit tests for the Book API endpoints.

This test module covers:
1. CRUD operations (Create, Retrieve, Update, Delete)
2. Filtering, searching, and ordering functionality
3. Authentication and permission controls
4. Response data integrity and status codes
to run future tests:
    python manage.py test api
    python manage.py test api --verbosity=2  # With details
    python manage.py test api.test_views.BookFilteringTestCase  # Specific class
Test Database:
- Uses Django's built-in test database (TestCase creates isolated transactions) using self.client.login
- Each test method runs in isolation with auto-rollback
- Fixtures (Author/Book objects) are created fresh for each test

API Endpoints:
- GET /api/books/ - List books with filtering/search/ordering
- GET /api/books/<pk>/ - Retrieve a single book
- POST /api/books/create/ - Create a new book (requires auth)
- PUT/PATCH /api/books/update/<pk>/ - Update a book (requires auth)
- DELETE /api/books/delete/<pk>/ - Delete a book (requires auth)
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.response import Response as DRFResponse
from typing import cast

from .models import Author, Book


class BookAPITestCase(TestCase):
    """Base test case with common setup for Book API tests."""

    # Tell static type-checkers this `client` is DRF's `APIClient` (has
    # `force_authenticate`). The instance is created in `setUp`.
    client: APIClient

    def setUp(self):
        """Set up test fixtures: users, authors, and books."""
        # Create test users
        self.auth_user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )

        # Create test authors
        self.author1 = Author.objects.create(name="George Orwell")
        self.author2 = Author.objects.create(name="J.R.R. Tolkien")
        self.author3 = Author.objects.create(name="Isaac Asimov")

        # Create test books
        self.book1 = Book.objects.create(
            title="1984", author=self.author1, publication_year=1949
        )
        self.book2 = Book.objects.create(
            title="Animal Farm", author=self.author1, publication_year=1945
        )
        self.book3 = Book.objects.create(
            title="The Hobbit", author=self.author2, publication_year=1937
        )
        self.book4 = Book.objects.create(
            title="Foundation", author=self.author3, publication_year=1951
        )

        # Initialize API client
        self.client = APIClient()

    # --- Typed request helpers ---
    def api_get(self, path, **kwargs) -> DRFResponse:
        client = TestCase.client.fget(self)  # Get the actual client instance
        return cast(DRFResponse, client.get(path, **kwargs))

    def api_post(self, path, data=None, **kwargs) -> DRFResponse:
        client = TestCase.client.fget(self)
        return cast(DRFResponse, client.post(path, data, **kwargs))

    def api_put(self, path, data=None, **kwargs) -> DRFResponse:
        client = TestCase.client.fget(self)
        return cast(DRFResponse, client.put(path, data, **kwargs))

    def api_patch(self, path, data=None, **kwargs) -> DRFResponse:
        client = TestCase.client.fget(self)
        return cast(DRFResponse, client.patch(path, data, **kwargs))

    def api_delete(self, path, **kwargs) -> DRFResponse:
        client = TestCase.client.fget(self)
        return cast(DRFResponse, client.delete(path, **kwargs))


class BookListTestCase(BookAPITestCase):
    """Test the BookListView (GET /api/books/)."""

    def test_list_books_unauthenticated(self):
        """Test that unauthenticated users can list books."""
        response = self.api_get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Response is a list, not paginated dict
        self.assertEqual(len(response.data), 4)

    def test_list_books_authenticated(self):
        """Test that authenticated users can list books."""
        self.client.force_authenticate(user=self.auth_user)
        response = self.api_get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_default_ordering_by_title(self):
        """Test that books are ordered by title by default."""
        response = self.api_get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, ["1984", "Animal Farm", "Foundation", "The Hobbit"])


class BookCreateTestCase(BookAPITestCase):
    """Test the BookCreateView (POST /api/books/create/)."""

    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books."""
        payload = {
            "title": "New Book",
            "author": "George Orwell",
            "publication_year": 2000,
        }
        response = self.api_post("/api/books/create/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        """Test that authenticated users can create books."""
        self.client.force_authenticate(user=self.auth_user)
        payload = {
            "title": "Brave New World",
            "author": "George Orwell",
            "publication_year": 1932,
        }
        response = self.api_post("/api/books/create/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Brave New World")
        self.assertTrue(Book.objects.filter(title="Brave New World").exists())

    def test_create_book_with_invalid_year(self):
        """Test that creating a book with a future year is rejected by validation."""
        self.client.force_authenticate(user=self.auth_user)
        payload = {
            "title": "Future Book",
            "author": "George Orwell",
            "publication_year": 2099,
        }
        response = self.api_post("/api/books/create/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", response.data.get("errors", {}))

    def test_create_book_with_invalid_author(self):
        """Test that creating a book with a non-existent author fails."""
        self.client.force_authenticate(user=self.auth_user)
        payload = {
            "title": "Mystery Book",
            "author": "Non Existent Author",
            "publication_year": 2000,
        }
        response = self.api_post("/api/books/create/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookDetailTestCase(BookAPITestCase):
    """Test the BookDetailView detail operations (GET /api/books/<pk>/)."""

    def test_retrieve_book_unauthenticated(self):
        """Test that unauthenticated users can retrieve a book."""
        response = self.api_get(f"/api/books/{self.book1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "1984")
        self.assertEqual(response.data["publication_year"], 1949)

    def test_retrieve_nonexistent_book(self):
        """Test that retrieving a non-existent book returns 404."""
        response = self.api_get("/api/books/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_book_authenticated(self):
        """Test that authenticated users can retrieve a book."""
        self.client.force_authenticate(user=self.auth_user)
        response = self.api_get(f"/api/books/{self.book1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "1984")


class BookUpdateTestCase(BookAPITestCase):
    """Test the BookUpdateView (PUT/PATCH /api/books/update/<pk>/)."""

    def test_update_book_unauthenticated(self):
        """Test that unauthenticated users cannot update books."""
        payload = {"title": "Updated Title"}
        response = self.api_patch(
            f"/api/books/update/{self.book1.pk}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated_full(self):
        """Test that authenticated users can fully update (PUT) a book."""
        self.client.force_authenticate(user=self.auth_user)
        payload = {
            "title": "Updated 1984",
            "author": "George Orwell",
            "publication_year": 1949,
        }
        response = self.api_put(
            f"/api/books/update/{self.book1.pk}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated 1984")
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated 1984")

    def test_update_book_authenticated_partial(self):
        """Test that authenticated users can partially update (PATCH) a book."""
        self.client.force_authenticate(user=self.auth_user)
        payload = {"title": "Patched 1984"}
        response = self.api_patch(
            f"/api/books/update/{self.book1.pk}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Patched 1984")
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Patched 1984")

    def test_update_book_with_invalid_year(self):
        """Test that updating a book with a future year is rejected."""
        self.client.force_authenticate(user=self.auth_user)
        payload = {
            "title": "1984",
            "author": "George Orwell",
            "publication_year": 2099,
        }
        response = self.api_put(
            f"/api/books/update/{self.book1.pk}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BookDeleteTestCase(BookAPITestCase):
    """Test the BookDeleteView (DELETE /api/books/delete/<pk>/)."""

    def test_delete_book_unauthenticated(self):
        """Test that unauthenticated users cannot delete books."""
        response = self.api_delete(f"/api/books/delete/{self.book1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists())

    def test_delete_book_authenticated(self):
        """Test that authenticated users can delete books."""
        self.client.force_authenticate(user=self.auth_user)
        book_id = self.book1.pk
        response = self.api_delete(f"/api/books/delete/{book_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=book_id).exists())


class BookFilteringTestCase(BookAPITestCase):
    """Test the filtering functionality (DjangoFilterBackend)."""

    def test_filter_by_title(self):
        """Test filtering books by exact title match."""
        response = self.api_get("/api/books/?title=1984")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "1984")

    def test_filter_by_author_name(self):
        """Test filtering books by author name (exact match via DjangoFilterBackend)."""
        response = self.api_get("/api/books/?author__name=George Orwell")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        titles = {book["title"] for book in response.data}
        self.assertEqual(titles, {"1984", "Animal Farm"})

    def test_filter_by_publication_year(self):
        """Test filtering books by publication year."""
        response = self.api_get("/api/books/?publication_year=1949")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "1984")

    def test_filter_multiple_fields(self):
        """Test combining multiple filters."""
        response = self.api_get(
            "/api/books/?author__name=George Orwell&publication_year=1949"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "1984")

    def test_filter_no_matches(self):
        """Test that filtering with no matches returns an empty list."""
        response = self.api_get("/api/books/?publication_year=2099")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class BookSearchTestCase(BookAPITestCase):
    """Test the search functionality (SearchFilter)."""

    def test_search_by_title(self):
        """Test searching books by title substring."""
        response = self.api_get("/api/books/?search=1984")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "1984")

    def test_search_by_author_name(self):
        """Test searching books by author name substring."""
        response = self.api_get("/api/books/?search=Orwell")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        titles = {book["title"] for book in response.data}
        self.assertEqual(titles, {"1984", "Animal Farm"})

    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        response = self.api_get("/api/books/?search=orwell")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_partial_match(self):
        """Test search with partial word matches."""
        response = self.api_get("/api/books/?search=Animal")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Animal Farm")

    def test_search_no_matches(self):
        """Test searching with no matches returns an empty list."""
        response = self.api_get("/api/books/?search=NonExistentBook")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class BookOrderingTestCase(BookAPITestCase):
    """Test the ordering functionality (OrderingFilter)."""

    def test_ordering_by_title_ascending(self):
        """Test ordering books by title in ascending order."""
        response = self.api_get("/api/books/?ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, ["1984", "Animal Farm", "Foundation", "The Hobbit"])

    def test_ordering_by_title_descending(self):
        """Test ordering books by title in descending order."""
        response = self.api_get("/api/books/?ordering=-title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, ["The Hobbit", "Foundation", "Animal Farm", "1984"])

    def test_ordering_by_publication_year_ascending(self):
        """Test ordering books by publication year in ascending order."""
        response = self.api_get("/api/books/?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, [1937, 1945, 1949, 1951])

    def test_ordering_by_publication_year_descending(self):
        """Test ordering books by publication year in descending order."""
        response = self.api_get("/api/books/?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, [1951, 1949, 1945, 1937])

    def test_ordering_combined_with_filter(self):
        """Test ordering combined with filtering."""
        response = self.api_get(
            "/api/books/?author__name=George Orwell&ordering=-publication_year"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, ["1984", "Animal Farm"])

    def test_ordering_combined_with_search(self):
        """Test ordering combined with searching."""
        response = self.api_get("/api/books/?search=Orwell&ordering=title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, ["1984", "Animal Farm"])


class BookPermissionTestCase(BookAPITestCase):
    """Test authentication and permission controls."""

    def test_list_allows_any(self):
        """Test that listing books allows any user (authenticated or not)."""
        # Unauthenticated
        response = self.api_get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Authenticated
        self.client.force_authenticate(user=self.auth_user)
        response = self.api_get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_allows_any(self):
        """Test that retrieving a book allows any user."""
        # Unauthenticated
        response = self.api_get(f"/api/books/{self.book1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Authenticated
        self.client.force_authenticate(user=self.auth_user)
        response = self.api_get(f"/api/books/{self.book1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_requires_authentication(self):
        """Test that creating a book requires authentication."""
        payload = {
            "title": "Test Book",
            "author": "George Orwell",
            "publication_year": 2000,
        }
        # Unauthenticated
        response = self.api_post("/api/books/create/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated
        self.client.force_authenticate(user=self.auth_user)
        response = self.api_post("/api/books/create/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_requires_authentication(self):
        """Test that updating a book requires authentication."""
        payload = {"title": "Updated Title"}
        # Unauthenticated
        response = self.api_patch(
            f"/api/books/update/{self.book1.pk}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated
        self.client.force_authenticate(user=self.auth_user)
        response = self.api_patch(
            f"/api/books/update/{self.book1.pk}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_requires_authentication(self):
        """Test that deleting a book requires authentication."""
        # Unauthenticated
        response = self.api_delete(f"/api/books/delete/{self.book1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated
        self.client.force_authenticate(user=self.auth_user)
        response = self.api_delete(f"/api/books/delete/{self.book1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authenticated_user_can_modify_any_book(self):
        """Test that any authenticated user can modify any book (no ownership check)."""
        self.client.force_authenticate(user=self.auth_user)
        payload = {"title": "Modified by First User"}
        response = self.api_patch(
            f"/api/books/update/{self.book1.pk}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Switch to different user and verify they can also modify
        self.client.force_authenticate(user=self.other_user)
        payload = {"title": "Modified by Second User"}
        response = self.api_patch(
            f"/api/books/update/{self.book1.pk}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BookDataIntegrityTestCase(BookAPITestCase):
    """Test response data integrity and consistency."""

    def test_create_response_includes_all_fields(self):
        """Test that the create response includes all book fields."""
        self.client.force_authenticate(user=self.auth_user)
        payload = {
            "title": "Test Book",
            "author": "George Orwell",
            "publication_year": 1950,
        }
        response = self.api_post("/api/books/create/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["title"], "Test Book")
        self.assertEqual(response.data["author"], "George Orwell")
        self.assertEqual(response.data["publication_year"], 1950)

    def test_retrieve_response_includes_all_fields(self):
        """Test that the retrieve response includes all book fields."""
        response = self.api_get(f"/api/books/{self.book1.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.book1.pk)
        self.assertEqual(response.data["title"], "1984")
        self.assertEqual(response.data["author"], "George Orwell")
        self.assertEqual(response.data["publication_year"], 1949)

    def test_list_response_structure(self):
        """Test that the list response is a list of book objects."""
        response = self.api_get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertTrue(len(response.data) > 0)
        self.assertIn("title", response.data[0])
        self.assertIn("author", response.data[0])

    def test_update_returns_updated_data(self):
        """Test that update returns the updated book data."""
        self.client.force_authenticate(user=self.auth_user)
        payload = {
            "title": "Updated Title",
            "author": "George Orwell",
            "publication_year": 1949,
        }
        response = self.api_put(
            f"/api/books/update/{self.book1.pk}/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")
        self.assertEqual(response.data["publication_year"], 1949)

