from django.contrib import admin
from .models import Book, CustomUser
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")
    search_fields = ("title", "author")
    list_filter = ("publication_year",)


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        "username",
        "email",
        "role",
        "date_of_birth",
        "is_staff",
        "is_active",
    )
    list_filter = ("role", "is_staff", "is_superuser", "is_active")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "date_of_birth",
                    "profile_picture",
                    "role",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "date_of_birth",
                    "profile_picture",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("username", "email", "role")
    ordering = ("username",)


# ✅ Explicit registration
admin.site.register(CustomUser, CustomUserAdmin)
