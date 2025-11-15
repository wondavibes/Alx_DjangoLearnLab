from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import CustomUser


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def set_default_role(sender, instance, created, **kwargs):
    if created and not instance.role:
        instance.role = "Member"
        instance.save()
