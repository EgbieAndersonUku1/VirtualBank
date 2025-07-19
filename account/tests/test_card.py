from secrets import token_hex
from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone
from django.core.exceptions import ValidationError

from account.utils.utils import current_year_choices
from freezegun import freeze_time


from ..models import BankAccount, Wallet, Card
from authentication.models import User
from ..utils.errors import WalletCardLimitExceededError
from utils.generator import generate_code


# Create your tests here.
def create_test_bank_account(user):
    bank_id = token_hex()
    bank = BankAccount.objects.create(bank_id=bank_id,
                                  sort_code=generate_code(6),
                                  account_number=generate_code(8),
                                  user=user                      
                                   )
        
    return bank

def create_test_card_model(card_id: str = "#12345678910", 
                      card_name: str = "John Doe", 
                      card_number: str = "1001-1001-2025-9874",
                      expiry_month: str = "JAN",
                      expiry_year: str = "2025",
                      card_options: str = "V",
                      card_type: str = "C",
                      cvc: str = "102",
                      bank_account=None,
                      wallet=None
                      ):
     
     return Card.objects.create(
            card_id=card_id,
            card_name=card_name,
            card_number=card_number,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
            card_options=card_options,
            card_type=card_type,
            cvc=cvc,
            bank_account=bank_account,
            wallet=wallet,
        )


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
        self.expiry_month  = Card.Month.APR.value
        self.expiry_year   = 2025
        self.card_options  = Card.CardOptions.VISA.value
        self.card_type     = Card.CardType.CREDIT.value
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


    def test_card_fields(self):
        """Test if the card fields are correctly saved"""
        self.card.refresh_from_db()

        self.assertEqual(self.card_name, self.card.card_name, "card_name does not match")
        self.assertEqual(self.card_number, self.card.card_number, "card_number does not match")
        self.assertEqual(self.expiry_month, self.card.expiry_month, "expiry_month does not match")
        self.assertEqual(self.expiry_year, self.card.expiry_year, "expiry_year does not match")
        self.assertEqual(self.card_options, self.card.card_options, "card_options does not match")
        self.assertEqual(self.card_type, self.card.card_type, "card_type does not match")
        self.assertEqual(self.cvc, self.card.cvc, "cvc does not match")
        self.assertEqual(self.bank_account, self.card.bank_account, "bank_account does not match")
        self.assertEqual(self.wallet, self.card.wallet, "wallet does not match")
     

        self.assertIsInstance(self.card.bank_account, BankAccount, "bank_account is not a BankAccount instance")
        self.assertIsInstance(self.card.wallet, Wallet, "wallet is not a Wallet instance")
    
    def test_card_id_exceeding_length_raises_error(self):
        """Test that an error is raised if the card_id exceeds max length (64)."""

        card_id = "i" * 74  # 74 characters, exceeds 64-char limit

        with self.assertRaises(ValidationError) as cm:
            card = create_test_card_model(card_id=card_id)
            card.full_clean()

        error = cm.exception

        # Check that 'card_id' is in the error dict
        self.assertIn('card_id', error.message_dict)

        # Check the specific message
        self.assertIn(
            "Ensure this value has at most 64 characters",
            error.message_dict['card_id'][0]
        )

    def test_card_name_exceeding_length_raises_error(self):
        """Test that an error is raised if the card name exceeds max length (64)."""
        
        card_name = "n" * 40 # 40 characters, exceeds 20-char limit

        with self.assertRaises(ValidationError) as cm:
            card = create_test_card_model(card_name=card_name)
            card.full_clean()

        error = cm.exception

        # Check that 'card_name' is in the error dict
        self.assertIn('card_name', error.message_dict)

        # Check the specific message
        self.assertIn(
            "Ensure this value has at most 20 characters",
            error.message_dict['card_name'][0]
        )

    def test_card_number_exceeding_length_raises_error(self):
        """Test that an error is raised if the card_number exceeds max length (20)."""
        
        card_number = "i" * 74  # 74 characters, exceeds 20-char limit

        with self.assertRaises(ValidationError) as cm:
            card = create_test_card_model(card_number=card_number)
            card.full_clean()

        error = cm.exception

        # Check that 'card_number' is in the error dict
        self.assertIn('card_number', error.message_dict)

        # Check the specific error message
        self.assertIn(
            "Ensure this value has at most 20 characters",
            error.message_dict['card_number'][0]
        )

    def test_valid_expiry_year_passes(self):
        valid_year = current_year_choices()[0][0]  # Get first valid year

        card = create_test_card_model(expiry_year=valid_year)
        try:
            card.full_clean()  # Should not raise
        except ValidationError:
            self.fail("ValidationError raised for a valid expiry year")

    def test_invalid_card_option_raises_error(self):
        invalid_option = "iiiiiii"  # Invalid: too long and not in choices

        with self.assertRaises(ValidationError) as cm:
            card = create_test_card_model(card_options=invalid_option)
            card.full_clean()

        error = cm.exception

        self.assertIn('card_options', error.message_dict)
        self.assertIn(
            "is not a valid choice",
            error.message_dict['card_options'][0]
        )

    def test_invalid_card_type_raises_error(self):
        invalid_option = "iiiiiii"  # Invalid: too long and not in choices

        with self.assertRaises(ValidationError) as cm:
            card = create_test_card_model(card_type=invalid_option)
            card.full_clean()

        error = cm.exception

        self.assertIn('card_type', error.message_dict)
        self.assertIn(
            "is not a valid choice",
            error.message_dict['card_type'][0]
        )
    
    def test_card_cvc_exceeding_length_raises_error(self):
        """Test that an error is raised if the card_cvc exceeds max length (3)."""
        
        invalid_cvc = "i" * 5 # 5 characters, exceeds 3-char limit

        with self.assertRaises(ValidationError) as cm:
            card = create_test_card_model(cvc=invalid_cvc)
            card.full_clean()

        error = cm.exception

        # Check that 'card_number' is in the error dict
        self.assertIn('cvc', error.message_dict)

        # Check the specific error message
        self.assertIn(
            "Ensure this value has at most 3 characters",
            error.message_dict['cvc'][0]
        )

    def test_raises_error_when_card_exceeds_storage_limit(self):
        """
        Test that saving a card raises an error when the wallet's card storage limit is exceeded.
        """

        bank_account = create_test_bank_account(self.user)
        wallet = Wallet.objects.create(
            wallet_id="12345672222",
            user=self.user,
            bank_account=bank_account
        )
    
        with self.assertRaises(WalletCardLimitExceededError) as cm:

             # card 1
            Card.objects.create(
                card_name="Jane Constantine",
                card_number="1234-9874-2011-2025",
                expiry_month=self.expiry_month,
                expiry_year=self.expiry_year,
                card_options=self.card_options,
                card_type=self.card_type,
                cvc=self.cvc,
                bank_account=bank_account,
                wallet=wallet,
            )

            # card 2
            Card.objects.create(
                card_name="Jane Doe",
                card_number="1234-9874-2011-2026",
                expiry_month=self.expiry_month,
                expiry_year=self.expiry_year,
                card_options=self.card_options,
                card_type=self.card_type,
                cvc=self.cvc,
                bank_account=bank_account,
                wallet=wallet,
            )
        
            # card 2
            Card.objects.create(
                card_name="John Doe",
                card_number="1234-9874-2011-2027",
                expiry_month=self.expiry_month,
                expiry_year=self.expiry_year,
                card_options=self.card_options,
                card_type=self.card_type,
                cvc=self.cvc,
                bank_account=bank_account,
                wallet=wallet,
            )

            # card 3
            Card.objects.create(
                card_name="EU",
                card_number="1234-9874-2011-2028",
                expiry_month=self.expiry_month,
                expiry_year=self.expiry_year,
                card_options=self.card_options,
                card_type=self.card_type,
                cvc=self.cvc,
                bank_account=bank_account,
                wallet=wallet,
            )

             # card 4 exceeds limit
            Card.objects.create(
                card_name="EU",
                card_number="1234-9874-2011-2029",
                expiry_month=self.expiry_month,
                expiry_year=self.expiry_year,
                card_options=self.card_options,
                card_type=self.card_type,
                cvc=self.cvc,
                bank_account=bank_account,
                wallet=wallet,
            )

    def test_get_by_wallet_method(self):
        """Test that a card is correctly retrieved usisng the wallet instance"""

        card = Card.get_by_wallet(self.wallet)
        self.assertIsInstance(card, Card, f"Expected an instance of Card but got {type(card)}")

    def test_get_by_bank_method(self):
        """Test that a card is correctly retrieved using the bank instance"""

        card = Card.get_by_bank(self.bank_account)
        self.assertIsInstance(card, Card, f"Expected an instance of Card but got {type(card)}")

        

