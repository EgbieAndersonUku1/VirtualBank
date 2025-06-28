from django.db import models
from django.core.validators import MinValueValidator


from authentication.models import User
from utils.generator import generate_code
from account.utils import current_year_choices

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
            models.indexes(fields=['sort_code', 'account_number'])
        ]

    @property
    def account_number(self):
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
        VISA        = "Visa",       "V"
        MASTER_CARD = "MasterCard", "M"
        DISCOVER    = "Discover",   "D"

    class CardType(models.TextChoices):
        CREDIT  = "Credit", "C"
        DEBIT   = "Debit", "D"

    card_name    = models.CharField(max_length=20)
    card_number  = models.CharField(max_length=16)
    expiry_month = models.CharField(choices=Month.choices, max_length=3)
    expiry_year  = models.PositiveBigIntegerField(choices=current_year_choices())
    card_options = models.CharField(choices=CardOptions.choices, max_length=1)
    card_type    = models.CharField(choices=CardOptions.choices, max_length=1)
    cvc          = models.CharField(max_length=3)
    account      = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="cards")



   

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