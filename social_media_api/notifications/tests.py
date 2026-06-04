from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.contrib.contenttypes.models import ContentType
from .models import Notification


class NotificationsAPITest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(username="alice", password="pass")
        self.user2 = User.objects.create_user(username="bob", password="pass")

        ct = ContentType.objects.get_for_model(User)
        self.notification = Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb="started following you",
            target_content_type=ct,
            target_object_id=self.user2.id,
        )

        self.client = APIClient()

    def test_list_notifications_shows_unread_first(self):
        self.client.force_authenticate(self.user1)
        resp = self.client.get("/notifications/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(isinstance(data, list))
        self.assertGreaterEqual(len(data), 1)
        # newest notification should be the one we created and unread
        self.assertEqual(data[0]["id"], self.notification.id)
        self.assertFalse(data[0]["is_read"])

    def test_unread_count_and_mark_read(self):
        self.client.force_authenticate(self.user1)
        resp = self.client.get("/notifications/unread_count/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get("unread_count"), 1)

        # mark as read
        resp = self.client.post(f"/notifications/{self.notification.id}/mark_read/")
        self.assertEqual(resp.status_code, 200)

        # unread count should now be zero
        resp = self.client.get("/notifications/unread_count/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get("unread_count"), 0)


from django.test import TestCase

# Create your tests here.
