from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookViewSet, BookList  # type: ignore

router = DefaultRouter()
router.register(r"books_all", BookViewSet, basename="book_all")

urlpatterns = [
    path("", include(router.urls)),
    path("books/", BookList.as_view(), name="book-list"),
    path("token-auth/", obtain_auth_token, name="api-token-auth"),
]
