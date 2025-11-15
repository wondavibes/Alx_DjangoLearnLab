from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from django.conf import settings


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


def profile_pic_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/profile_pics/user_<id>/<filename>
    return f"profile_pics/user_{instance.id}/{filename}"


class CustomUserManager(UserManager):
    """Custom manager that works with AbstractUser."""

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        extra_fields.setdefault("role", "Member")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "Admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    ]
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to=profile_pic_path, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="Member")

    objects = CustomUserManager()  # now type-compatible

    def _str_(self):
        return f"{self.username} ({self.role})"
