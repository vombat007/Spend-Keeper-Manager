from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .utils import create_default_categories


@receiver(post_save, sender=User)
def create_user_default_categories(sender, instance, created, **kwargs):
    if created:
        create_default_categories(instance)
