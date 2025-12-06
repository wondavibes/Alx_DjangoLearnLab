from django.contrib import admin
from .models import Post, Profile


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "published_date"]
    list_filter = ["published_date", "author"]
    search_fields = ["title", "content"]
    readonly_fields = ["published_date"]
    fieldsets = (
        ("Post Info", {"fields": ("title", "content", "author")}),
        ("Publishing", {"fields": ("published_date",)}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "bio"]
    search_fields = ["user__username", "bio"]
    readonly_fields = ["user"]
