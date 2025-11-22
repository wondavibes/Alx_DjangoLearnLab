# models.py
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from typing import Any


def profile_pic_path(instance, filename):
    return f"profile_pics/{instance.username}/{filename}"


class CustomUserManager(UserManager):
    def create_user(
        self,
        username: str,
        email: str | None = None,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "CustomUser":
        if not username:
            raise ValueError("The Username must be set")
        extra_fields.setdefault("role", "Member")
        user = self.model(username=username, email=email or "", **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        username: str,
        email: str | None = None,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "CustomUser":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "Admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    ]

    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to=profile_pic_path, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Member")

    objects = CustomUserManager()

    def _str_(self):
        return f"{self.username} ({self.role})"


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author}, {self.publication_year}"

    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
