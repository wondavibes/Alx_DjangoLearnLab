from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        blank=True,
        null=True,
        help_text="Profile picture of the user",
    )

    # user.followers → people who follow this user

    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following_set", blank=True
    )

    def __str__(self):
        return self.username
