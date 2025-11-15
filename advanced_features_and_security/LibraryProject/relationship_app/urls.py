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
    # Authentication: use the custom login view so redirection is role-aware
    path(
        "login/",
        views.CustomLoginView.as_view(template_name="relationship_app/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="relationship_app/logout.html"),
        name="logout",
    ),
    # Homepage offering role-specific login links
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("admin_view/", admin_view, name="admin_view"),
    path("librarian_view/", librarian_view, name="librarian_view"),
    path("member_view/", member_view, name="member_view"),
    path("add_book/", add_book, name="add_book"),
    path("edit_book/<int:pk>/", edit_book, name="edit_book"),
    path("delete_book/<int:pk>/", delete_book, name="delete_book"),
]
