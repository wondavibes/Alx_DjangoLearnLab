from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookList  # type: ignore

router = DefaultRouter()
router.register(r"books_all", BookViewSet, basename="book_all")

urlpatterns = [
    path("", include(router.urls)),
    path("books/", BookList.as_view(), name="book-list"),
]
