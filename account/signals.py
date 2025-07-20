import logging

from django.db.models.signals import post_save, pre_save
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError

from django.dispatch import receiver
from secrets import token_hex

from .models import Profile, BankAccount, Wallet, Card
from utils.generator import generate_code
from .utils.errors import WalletCardLimitExceededError


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=BankAccount)
def initialize_bank_account_fields(sender, instance, **kwargs):
    
    if not instance.bank_id:
        instance.bank_id = token_hex()
    if not instance.account_number:
        instance.account_number = generate_code(9)
    if not instance.sort_code:
        instance.sort_code = generate_code(6)



@receiver(pre_save, sender=Card)
def initialize_card_id(sender, instance, **kwargs):
    
    if not instance.card_id:
        instance.card_id = token_hex()
   

@receiver(post_save, sender=Profile)
def create_bank_and_wallet(sender, instance, created, **kwargs):

    if created:

        try:

            with transaction.atomic():
                bank_account = BankAccount.objects.create(user=instance.user)
                Wallet.objects.create(user=instance.user, bank_account=bank_account)

        except IntegrityError as e:
            logger.error(f"Error creating Bank or Wallet for UserProfile {instance.pk}: {e}")

            

@receiver(pre_save, sender=Wallet)
def create_wallet_id(sender, instance, *args, **kwargs):

    if instance:
        if not instance.wallet_id:
            instance.wallet_id = token_hex()



@receiver(pre_save, sender=Profile)
def create_profile_id(sender, instance, *args, **kwargs):

    
    if instance:
        if not instance.profile_id:
            instance.profile_id = token_hex()
        if not instance.email:
            instance.email = instance.user.email.lower()
        


@receiver(pre_save, sender=Card)
def check_if_wallet_card_storage_has_exceeded(sender, instance, *args, **kwargs):

    if not instance.card_id:
        instance.card_id = token_hex()
    
          
