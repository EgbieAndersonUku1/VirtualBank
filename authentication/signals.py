from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import User


@receiver(pre_save, sender=User)
def pre_save_username(sender, instance, *args, **kwargs):
    
    if instance:
        instance.email      = instance.email.lower()
        instance.username   = instance.username.lower()

    



