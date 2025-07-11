from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import User, Verification
from account.models import BankAccount, Profile


@receiver(pre_save, sender=User)
def pre_save_username(sender, instance, *args, **kwargs):
    
    if instance:
        instance.email      = instance.email.lower()
        instance.username   = instance.username.lower()

    



