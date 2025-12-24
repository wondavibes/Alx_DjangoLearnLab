from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from django.db.models import QuerySet


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[Notification]:
        # Order unread notifications first, then by newest timestamp
        # `is_read` is False for unread; ordering ascending puts unread before read.
        return Notification.objects.filter(recipient=self.request.user).order_by(
            "is_read", "-timestamp"
        )

    @action(detail=False, methods=["get"])
    def unread(self, request):
        unread_notifications = (
            self.get_queryset().filter(is_read=False).order_by("-timestamp")
        )
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def unread_count(self, request):
        """Return the current user's unread notification count."""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({"unread_count": count})

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"detail": "Notification marked as read."})
