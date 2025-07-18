from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from freezegun import freeze_time


from ..models import BankAccount, Wallet, Card
from authentication.models import User
from ..utils.errors import WalletCardLimitExceededError

# Create your tests here.

@freeze_time("2025-07-14 16:00:00")
class CardTest(TestCase):

    def setUp(self):
    
        self.user = User.objects.create(
                                first_name="Test name",
                                surname="Test surname",
                                username="Test username",
                                email="test@example.com",
                                pin="1234"
                                )

    
        self.bank_account  = BankAccount.objects.create(bank_id="123456789",
                                                         sort_code="40014",
                                                         account_number="01212409",
                                                         user=self.user
                                                         )
        
        self.wallet = Wallet.objects.create(
            wallet_id="123456789",
            user=self.user,
            bank_account=self.bank_account
        )

        self.card_name     = "John Doe"
        self.card_number   = "1234-1234-5678-1011"
        self.expiry_month  = Card.Month.APR
        self.expiry_year   = "2025"
        self.card_options  = Card.CardOptions.VISA
        self.card_type     = Card.CardType.CREDIT
        self.cvc           = "101"

        self.card = Card.objects.create(
            card_name=self.card_name,
            card_number=self.card_number,
            expiry_month=self.expiry_month,
            expiry_year=self.expiry_year,
            card_options=self.card_options,
            card_type=self.card_type,
            cvc=self.cvc,
            bank_account=self.bank_account,
            wallet=self.wallet,
        )

  
    def test_creation_count(self):
        """Test if the bank account object was successfully created"""

        # test bank creation and creation count
        self.assertTrue(BankAccount.objects.filter(bank_id=self.bank_account.bank_id).exists(), msg="Expected a bank account object")
        self.assertEqual( BankAccount.objects.count(), 1,  msg="Expected a single creation count")

        # test user creation and creation count
        self.assertTrue(User.objects.filter(email=self.user.email).exists(), msg="Expected a user object")
        self.assertEqual(User.objects.count(), 1, msg="Expected a single creation count")

        # test wallet creation and creation count
        self.assertTrue(Wallet.objects.filter(wallet_id=self.wallet.wallet_id).exists(), msg="Expected a wallet object")
        self.assertEqual(Wallet.objects.count(), 1, msg="Expected a single creation count")

        # test if the card is created
        self.assertTrue(Card.objects.filter(card_number=self.card_number).exists())
        self.assertEqual(Card.objects.count(), 1, msg="Expected a single creation count")
    
    def test_num_of_card_in_wallet(self):

        self.wallet.refresh_from_db()

        self.assertEqual(self.wallet.num_of_cards_added, 1)

        Card.objects.create(
            card_name="Jane Doe",
            card_number="1234-9874-2011-2025",
            expiry_month=self.expiry_month,
            expiry_year=self.expiry_year,
            card_options=self.card_options,
            card_type=self.card_type,
            cvc=self.cvc,
            bank_account=self.bank_account,
            wallet=self.wallet,
        )

        # add another card to the wallet
        self.assertEqual(self.wallet.num_of_cards_added, 2)

    def test_card_is_connected_to_wallet(self):

        self.assertIsNotNone(self.card.wallet, msg="Expected the card to be linked to a wallet")
        self.assertEqual(self.card.wallet, self.wallet, msg="Card is not linked to the expected wallet")
      

