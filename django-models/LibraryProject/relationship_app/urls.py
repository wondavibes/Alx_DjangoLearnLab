from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import list_books, LibraryDetailView

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
]
