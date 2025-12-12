# posts/permissions.py
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # SAFE METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only the author can edit/delete
        return obj.author == request.user
