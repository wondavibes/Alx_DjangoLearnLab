# social_media_api/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # All accounts endpoints under /api/accounts/
    path("api/accounts/", include("accounts.urls")),
    # All posts & comments endpoints under /api/
    path("api/", include("posts.urls")),
    # all notifications
    path("api/", include("notifications.urls"))
]
