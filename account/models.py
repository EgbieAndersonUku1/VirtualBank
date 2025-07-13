from typing import Optional
from django.db import models
from django.core.validators import MinValueValidator

from authentication.models import User
from utils.generator import generate_code
from .utils.utils import current_year_choices, profile_to_dict


# Create your models here.

class BankAccount(models.Model):
    bank_id        = models.CharField(max_length=40, unique=True, db_index=True, blank=True, null=True)
    sort_code      = models.CharField(max_length=6, unique=True, db_index=True, blank=True)
    account_number = models.CharField(max_length=8, unique=True, db_index=True, blank=True)
    amount         = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(0)], default=0)
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account")
    created_on     = models.DateTimeField(auto_now_add=True)
    modified_on    = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['sort_code', 'account_number'])
        ]

    def __str__(self):
        return f"{self.sort_code}{self.account_number}"

    @property
    def username(self):
        return self.user.username
    
    @property
    def email(self):
        return self.user.email
    
    @property
    def full_account_number(self):
        return f"{self.sort_code}{self.account_number}"
    
    @property
    def pin(self):
        return self.user.pin
    
    @classmethod
    def get_by_account_number(cls, sort_code, account_number):
        
        try:
            return cls.objects.get(sort_code=sort_code, account_number=account_number)
        except cls.DoesNotExist:
            return None
        
    @classmethod
    def get_by_user(cls, user):
        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            return None
    
    def add_amount(amount: float) -> None:
        pass

    def deduct_amount(amount: float) -> None:
        pass


  
class Card(models.Model):

    class Month(models.TextChoices):
        JAN = "JAN", "January"
        FEB = "FEB", "February"
        MAR = "MAR", "March"
        APR = "APR", "April"
        MAY = "MAY", "May"
        JUN = "JUN", "June"
        JUL = "JUL", "July"
        AUG = "AUG", "August"
        SEP = "SEP", "September"
        OCT = "OCT", "October"
        NOV = "NOV", "November"
        DEC = "DEC", "December"

    class CardOptions(models.TextChoices):
        VISA        = "V", "Visa"
        MASTER_CARD = "M", "MasterCard"
        DISCOVER    = "D", "Discover"

    class CardType(models.TextChoices):
        CREDIT = "C", "Credit"
        DEBIT  = "D", "Debit"


    card_name    = models.CharField(max_length=20)
    card_number  = models.CharField(max_length=16)
    expiry_month = models.CharField(choices=Month.choices, max_length=3)
    expiry_year  = models.PositiveBigIntegerField(choices=current_year_choices())
    card_options = models.CharField(choices=Month.choices, max_length=3)
    card_type    = models.CharField(choices=CardType.choices, max_length=1)
    cvc          = models.CharField(max_length=3)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="card")
    account      = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="cards")
    created_on   = models.DateTimeField(auto_now_add=True)
    modified_on  = models.DateTimeField(auto_now=True)

    def add_amount(amount: float) -> None:
        pass

    def deduct_amount(amount: float) -> None:
        pass



class Wallet(models.Model):
    wallet_id             = models.CharField(max_length=64, unique=True, db_index=True)
    amount                = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(0)], default=0)
    cards                 = models.ForeignKey(Card, on_delete=models.SET_NULL, blank=True, null=True, related_name="wallet")
    total_cards           = models.SmallIntegerField(validators=[MinValueValidator(0)], default=0, blank=True, null=True)
    last_amount_received  = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(0)], default=0)
    maximum_cards         = models.SmallIntegerField(validators=[MinValueValidator(0)], default=3)
    user                  = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, blank=True, null=True)
    bank_account          = models.ForeignKey(BankAccount, models.SET_NULL, blank=True, null=True, db_index=True)
    created_on            = models.DateTimeField(auto_now_add=True)
    modified_on           = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["wallet_id", "user", "bank_account"])
        ]

    def __str__(self):
        return self.wallet_id

    @property
    def pin(self):
        return self.user.pin
    
    @property
    def email(self):
        return self.user.email 
    
    @property
    def username(self):
        return self.user.username
    
    @classmethod
    def get_by_wallet_id(cls, wallet_id):
        """"""
        return cls._get_by_helper("wallet_id", wallet_id)

    @classmethod
    def get_by_bank(cls, bank):
        return cls._get_by_helper("bank", bank)
    
    @classmethod
    def get_by_user(cls, user):
        return cls._get_by_helper("user", user)

    @classmethod
    def _get_by_helper(cls, field_name, field_value):
        try:
            if field_name == "bank":
                return cls.objects.get(bank_account=field_value)
            if field_name == "user":
                return cls.objects.get(user=field_value)
            if field_name == "wallet_id":
                return cls.objects.get(wallet_id=field_value)
        except cls.DoesNotExist:
            return
        
    @property
    def is_bank_connected(self):
        return self.bank is not None

    def add_amount(amount: float) -> None:
        pass

    def deduct_amount(amount: float) -> None:
        pass



class Profile(models.Model):

    class Gender(models.TextChoices):
        
        SELECT_GENDER = "", "Select your gender"
        MALE          = "M", "Male"
        FEMALE        = "F", "Femaie"
        OTHER         = "O", "Other"
        PREFER_NOT_TO_SAY = "P", "Prefer not to say"

    class Maritus_Status(models.TextChoices):

        SELECT_YOUR_STATUS         = "", "Select your status"
        SINGLE                     = "S", "Single"
        MARRIED                    = "M", "Married"
        DIVORCED                   = "D", "Divorced"
        WIDOWED                    = "W", "Widowed"
        SEPARATED                  = "SD", "Separated"
        IN_A_RELATIONSHIP          = "I", "In a relationship"
        ENGAGED                    = "E", "Engaged"
        IN_A_CIVIL_PARTNERSHIP     = "IACP", "In a civil partnership"
        IN_A_DOMESTIC_PARTNERSHIP  = "IADP", "In a domestic partnership"
        ITS_COMPLICATED            = "IC", "It's complicated"
        PREFER_NOT_TO_SAY          = "P", "Prefer not to say"

    class IdentificationType(models.TextChoices):
        PASSPORT        = "p", "Passport"
        DRIVING_LICENCE = "d", "Driving Licence"
        NATIONAL_ID     = "n", "National ID"
    
    class Signature(models.TextChoices):
        UPLOAD_SIGNATURE = "u", "Upload signature"
        DRAW_SIGNATURE   = "d", "Draw signature"

    profile_id               = models.CharField(max_length=64, unique=True, blank=True, null=True, db_index=True)
    first_name               = models.CharField(max_length=40)
    surname                  = models.CharField(max_length=40)
    email                    = models.EmailField(max_length=40, blank=True)
    mobile                   = models.CharField(max_length=20)
    country                  = models.CharField(max_length=50)
    state                    = models.CharField(max_length=50)
    postcode                 = models.CharField(max_length=10)
    gender                   = models.CharField(choices=Gender.choices, max_length=1)
    maritus_status           = models.CharField(choices=Maritus_Status.choices, max_length=4)
    user                     = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, db_index=True, related_name="profile")
    identification_documents = models.CharField(choices=IdentificationType.choices, max_length=1)
    signature                = models.CharField(choices=Signature.choices, max_length=1)
    created_on              = models.DateTimeField(auto_now_add=True)
    modified_on             = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.first_name and self.surname:
          return f"{self.first_name.title()}{self.surname.title()}"
    
    @classmethod
    def get_by_user(cls, user: User) -> Optional[User]:
        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            return None

    def to_json(self):
       return profile_to_dict(self)



class TransferService:

    @classmethod
    def transfer_from_card_to_bank(cls, card: Card, bank_account: BankAccount, amount: float) -> bool:
        cls._validate_card(card)
        cls._validate_bank_account(bank_account)
        cls._is_amount_valid(amount)

        # to be added
    
    @classmethod
    def transfer_from_bank_to_wallet(cls, bank_account: BankAccount, wallet: Wallet, amount: float):
        cls._validate_bank_account(bank_account)
        cls._validate_wallet(wallet)
        cls._is_amount_valid(amount)
         # to be added

    @classmethod
    def transfer_from_wallet_to_bank(cls, bank_account: BankAccount, wallet: Wallet, amount: float) -> bool:
        cls._validate_bank_account(bank_account)
        cls._validate_wallet(wallet)
        cls._is_amount_valid(amount)

        # to be added

    @classmethod
    def transfer_funds_between_cards(cls, source_card: Card, target_card: Card, amount):
        cls._validate_card(source_card)
        cls._validate_card(target_card)
        cls._is_amount_valid(amount)

    @staticmethod
    def _is_amount_valid(amount: float) -> bool:
        pass

    @staticmethod
    def _validate_bank_account(bank_account: BankAccount):
        pass

    @staticmethod
    def _validate_wallet(wallet: Wallet):
        pass

    @staticmethod
    def _validate_card(card: Card):
        pass

