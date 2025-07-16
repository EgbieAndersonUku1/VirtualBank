from typing import Optional
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from authentication.models import User
from utils.generator import generate_code
from .utils.utils import current_year_choices, profile_to_dict
from .utils.errors import (BankInsufficientFundsError,
                            WalletInsufficientFundsError, 
                            BankAccountIsNotConnectedToWalletError
                            )


# Create your models here.


class BalanceMixin:
    amount_field: str = "amount"  # Default, but can be overridden in child classes

    def _get_amount(self) -> float:
        self._validate_amount_field()
        return getattr(self, self.amount_field)

    def _set_amount(self, new_amount: float) -> None:
        self._is_amount_valid(new_amount)
        setattr(self, self.amount_field, new_amount)
        self.save(update_fields=[self.amount_field])

    def add_amount(self, amount: float) -> None:
        current = self._get_amount()
        self._set_amount(current + amount)

    def deduct_amount(self, amount: float, ExceptionErrorClass: type[Exception], message: str = None) -> None:
        current = self._get_amount()
        if amount > current:
            raise ExceptionErrorClass(message)
        self._set_amount(current - amount)

    def _is_amount_valid(self, amount: float) -> bool:
        if not isinstance(amount, (float, int, Decimal)):
            raise TypeError(f"The amount must be type float, int or decimal but got type {type(amount)}")
        return True
    
    def _validate_amount_field(self) -> None:
        if not hasattr(self, self.amount_field):
            raise ValueError(f"{self.__class__.__name__} must define a '{self.amount_field}' field.")
        


class BankAccount(BalanceMixin, models.Model):
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
        return self.full_account_number

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
    
    def deduct_amount(self, amount: float) -> None:
        message = f"Insufficient amount for withdrawal, current amount: {self.amount}, withdrawal amount: {amount}, overdrawn: {self.amount - amount}"
        super().deduct_amount(amount, BankInsufficientFundsError, message)


  
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
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="card", blank=True, null=True)
    wallet       = models.ForeignKey("Wallet", on_delete=models.SET_NULL, blank=True, null=True, related_name="cards")
    account      = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="cards")
    created_on   = models.DateTimeField(auto_now_add=True)
    modified_on  = models.DateTimeField(auto_now=True)

  


class Wallet(BalanceMixin, models.Model):
    wallet_id             = models.CharField(max_length=64, unique=True, db_index=True)
    amount                = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(0)], default=0)
    total_cards           = models.SmallIntegerField(validators=[MinValueValidator(0)], default=0, blank=True, null=True)
    last_amount_received  = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(0)], default=0)
    maximum_cards         = models.SmallIntegerField(validators=[MinValueValidator(0)], default=3)
    user                  = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, blank=True, null=True)
    bank_account          = models.OneToOneField(BankAccount, models.SET_NULL, blank=True, null=True, db_index=True)
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
        return cls._get_by_helper("wallet_id", wallet_id)

    @classmethod
    def get_by_bank(cls, bank):
        # This returns a queryset because multiple wallets can have the same bank account
        return cls._get_by_helper("bank", bank)

    @classmethod
    def get_by_user(cls, user):
        return cls._get_by_helper("user", user)

    @classmethod
    def _get_by_helper(cls, field_name, field_value):
        """
        Helper method to retrieve Wallet instances filtered by a specified field.

        This method optimises database access by using `select_related` to 
        fetch related `User` and `BankAccount` objects in the same query, 
        reducing the number of database hits. This means that the related user 
        and bank account models are retrieved in a single query. Without 
        `select_related`, accessing `wallet.bank_account` or `wallet.user` after
        the model has been queried would trigger additional database queries, 
        leading to the N + 1 query problem.


        Example:
        Without `select_related` (causes N + 1 queries):

            wallet = Wallet.objects.filter(bank_account=bank)
            
            #now if I was to do this 
            print(wallet.user.email)  # Each access triggers a separate DB query

        With `select_related` (only 1 query):

            wallets = Wallet.objects.select_related('user', 'bank_account').filter(bank_account=bank)
        
            print(wallet.user.email)  # No extra queries; related objects already fetched

        Using this helper method which applies `select_related` internally:

            wallets = Wallet._get_by_helper("bank", bank)
            for wallet in wallets:
                print(wallet.user.email)

        Args:
            field_name (str): The field to filter by. Supported values are:
                - "bank": returns a QuerySet of Wallets filtered by bank_account.
                - "user": returns a single Wallet instance filtered by user.
                - "wallet_id": returns a single Wallet instance filtered by wallet_id.
            field_value: The value to filter the field by.

        Returns:
            QuerySet or Wallet instance or None:
                - For "bank": returns a QuerySet of Wallets associated with the bank_account.
                - For "user" and "wallet_id": returns a single Wallet instance or None if not found.

        Raises:
            DoesNotExist: When a Wallet with the given user or wallet_id does not exist (caught and returns None).
        """
        qs = cls.objects.select_related('user', 'bank_account')
        try:
            if field_name == "bank":
                return qs.filter(bank_account=field_value)
            if field_name == "user":
                return qs.get(user=field_value)
            if field_name == "wallet_id":
                return qs.get(wallet_id=field_value)
        except cls.DoesNotExist:
            return None

    @property
    def is_bank_connected(self):
        return self.bank_account is not None
    
    def deduct_amount(self, amount: float) -> None:
        super().deduct_amount(amount, WalletInsufficientFundsError)
     



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

        if not wallet.is_bank_connected:
            raise BankAccountIsNotConnectedToWalletError()
        
        wallet.deduct_amount(amount)
        bank_account.add_amount(amount)
        return True
        

        
   


    @classmethod
    def transfer_funds_between_cards(cls, source_card: Card, target_card: Card, amount):
        cls._validate_card(source_card)
        cls._validate_card(target_card)
        cls._is_amount_valid(amount)

    @staticmethod
    def _is_amount_valid(amount: float) -> bool:
        if not isinstance(amount, (float, int)):
            raise TypeError(f"The amount must be type float, int or decimal but got type {type(amount)}")
        return True

    @staticmethod
    def _validate_bank_account(bank_account: BankAccount):
        pass

    @staticmethod
    def _validate_wallet(wallet: Wallet):
        pass

    @staticmethod
    def _validate_card(card: Card):
        pass

