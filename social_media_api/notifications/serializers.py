# notificatiobns/serializers.py
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source="actor.username", read_only=True)
    target_repr = serializers.StringRelatedField(source="target", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "actor_username",
            "verb",
            "target_repr",
            "timestamp",
            "is_read",
        ]
        read_only_fields = ["recipient", "actor_username", "verb", "timestamp"]
