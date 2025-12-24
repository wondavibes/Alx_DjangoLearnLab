# social_media_api/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # All accounts endpoints under /api/accounts/
    path("api/accounts/", include("accounts.urls")),
    # All posts & comments endpoints under /api/
    path("api/", include("posts.urls")),
    # all notifications (mounted at root /notifications/ instead of under /api/)
    path("notifications/", include("notifications.urls")),
]
