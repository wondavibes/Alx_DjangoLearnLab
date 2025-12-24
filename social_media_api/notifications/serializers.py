# notificatiobns/serializers.py
from rest_framework import serializers
from .models import Notification
from django.utils.timesince import timesince


class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source="actor.username", read_only=True)
    target_repr = serializers.StringRelatedField(source="target", read_only=True)
    actor_avatar = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "actor_username",
            "actor_avatar",
            "verb",
            "target_repr",
            "timestamp",
            "time_since",
            "is_read",
        ]
        read_only_fields = ["recipient", "actor_username", "verb", "timestamp"]

    def get_actor_avatar(self, obj):
        actor = getattr(obj, "actor", None)
        if not actor:
            return None
        pic = getattr(actor, "profile_picture", None)
        if not pic:
            return None
        try:
            return pic.url
        except Exception:
            return None

    def get_time_since(self, obj):
        # returns a human-friendly relative time like "3 minutes"
        if not obj.timestamp:
            return None
        return f"{timesince(obj.timestamp)} ago"
