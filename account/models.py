from django.db import models
from django.core.validators import MinValueValidator


from authentication.models import User
from utils.generator import generate_code
from .utils.utils import current_year_choices

# Create your models here.

class BankAccount(models.Model):

    sort_code      = models.CharField(max_length=6, unique=True, db_index=True, default=generate_code(maximum_length=6))
    account_number = models.CharField(max_length=8, unique=True, db_index=True, default=generate_code(maximum_length=8))
    amount         = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(0)])
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account")
    created_on     = models.DateTimeField(auto_now_add=True)
    modified_on    = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['sort_code', 'account_number'])
        ]


    @property
    def full_account_number(self):
        return f"{self.sort_code}{self.account_number}"
    
    @property
    def pin(self):
        return self.user.pin
    


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
    account      = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="cards")
    created_on   = models.DateTimeField(auto_now_add=True)
    modified_on  = models.DateTimeField(auto_now=True)


class Wallet(models.Model):
    wallet_id             = models.CharField(default=generate_code(maximum_length=11), unique=True)
    amount                = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(0)])
    cards                 = models.ForeignKey(Card, on_delete=models.CASCADE)
    total_cards           = models.SmallIntegerField(validators=[MinValueValidator(0)])
    last_transfer         = models.DateTimeField(auto_now=True)
    last_amount_received  = models.DecimalField(max_digits=10,decimal_places=2, validators=[MinValueValidator(0)])
    maximum_cards         = models.SmallIntegerField(validators=[MinValueValidator(0)])
    created_on            = models.DateTimeField(auto_now_add=True)
    modified_on           = models.DateTimeField(auto_now=True)


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

    first_name               = models.CharField(max_length=40)
    surname                  = models.CharField(max_length=40)
    email                    = models.EmailField(max_length=40, blank=True)
    mobile                   = models.CharField(max_length=20)
    country                  = models.CharField(max_length=50)
    state                    = models.CharField(max_length=50)
    postcode                 = models.CharField(max_length=10)
    gender                   = models.CharField(choices=Gender.choices, max_length=1)
    maritus_status           = models.CharField(choices=Maritus_Status.choices, max_length=4)
    user                     = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    identification_documents = models.CharField(choices=IdentificationType.choices, max_length=1)
    signature                = models.CharField(choices=Signature.choices, max_length=1)
    created_on              = models.DateTimeField(auto_now_add=True)
    modified_on             = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = self.user.email.lower()
        return super().save(*args, **kwargs)