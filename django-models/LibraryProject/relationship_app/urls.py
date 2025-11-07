from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    list_books,
    LibraryDetailView,
    admin_view,
    librarian_view,
    member_view,
    add_book,
    edit_book,
    delete_book,
)


# already imported views directly above so no need to write views.list_books or views.LibraryDetailView
urlpatterns = [
    path("books/", list_books, name="list_books"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    # Authentication
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
    path("", views.register, name="register"),
    path("admin-view/", admin_view, name="admin_view"),
    path("librarian-view/", librarian_view, name="librarian_view"),
    path("member-view/", member_view, name="member_view"),
    path("add-book/", add_book, name="add_book"),
    path("edit-book/<int:pk>/", edit_book, name="edit_book"),
    path("delete-book/<int:pk>/", delete_book, name="delete_book"),
]
