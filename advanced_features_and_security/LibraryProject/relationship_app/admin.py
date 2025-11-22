from django.contrib import admin
from .models import Librarian, Library, Book, Author
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ("name", "librarian")
    search_fields = ("name", "librarian__name")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author")
    search_fields = ("title", "author__name")


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ("name", "library")
    search_fields = ("name", "library__name")


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
