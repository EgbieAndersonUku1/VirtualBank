from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from freezegun import freeze_time


from ..models import BankAccount, Wallet, TransferService
from authentication.models import User
from ..utils.errors import BankAccountIsNotConnectedToWalletError


# Create your tests here.

@freeze_time("2025-07-14 16:00:00")
class WalletTest(TestCase):

    def setUp(self):
        self.email          = "test@example.com"
        self.user           = User.objects.create(
                                first_name="Test name",
                                surname="Test surname",
                                username="Test username",
                                email=self.email,
                                pin="1234"
                                )
        self.bank_id        = "123456789"
        self.sort_code      = "400147"
        self.account_number = "01232789"
        self.amount         = 100
        self.bank_account   = BankAccount.objects.create(bank_id=self.bank_id,
                                                         sort_code=self.sort_code,
                                                         account_number=self.account_number,
                                                         amount=self.amount,
                                                         user=self.user
                                                         )
        
        self.wallet_id = "123456789"
        self.wallet = Wallet.objects.create(
            wallet_id=self.wallet_id,
            user=self.user,
            bank_account=self.bank_account
        )
  
    def test_creation_count(self):
        """Test if the bank account object was successfully created"""

        # test bank creation and creation count
        self.assertTrue(BankAccount.objects.filter(bank_id=self.bank_id).exists(), msg="Expected a bank account object")
        self.assertEqual( BankAccount.objects.count(), 1,  msg="Expected a single creation count")

        # test user creation and creation count
        self.assertTrue(User.objects.filter(email=self.email).exists(), msg="Expected a user object")
        self.assertEqual(User.objects.count(), 1, msg="Expected a single creation count")

        # test wallet creation and creation count
        self.assertTrue(Wallet.objects.filter(wallet_id=self.wallet_id).exists(), msg="Expected a wallet object")
        self.assertEqual(Wallet.objects.count(), 1, msg="Expected a single creation count")

    def test_email_property_returns_user_email(self):
        self.assertEqual(self.wallet.email, self.email)

    def test_username_property_returns_user_email(self):
        self.assertEqual(self.wallet.username, self.user.username)

    def test_pin_property_returns_user_pin(self):
        self.assertEqual(self.wallet.pin, self.user.pin)

    def test_wallet_account_fields(self):
        """Test if the fields are save correctly in the database"""

        # refresh the model so it pulls from the database and not the saved instance
        self.bank_account.refresh_from_db()

        self.assertEqual(self.wallet.wallet_id, self.wallet_id)
        self.assertEqual(self.wallet.amount, 0)
        self.assertEqual(self.wallet.total_cards, 0)
        self.assertEqual(self.wallet.last_amount_received, 0)
        self.assertEqual(self.wallet.maximum_cards, 3)
        self.assertIsInstance(self.wallet.bank_account, BankAccount)
        self.assertIsInstance(self.wallet.user, User)

        # frozen time check
        frozen_time = timezone.now()

        self.assertEqual(self.wallet.created_on, frozen_time)
        self.assertEqual(self.wallet.modified_on, frozen_time)
    
    def test_add_amount(self):
        """Test if the amount is correctly add to the wallet"""

        # refresh the model so it pulls from the database and not the saved instance
        self.wallet.refresh_from_db()

        AMOUNT_ADDED    = 100
        EXPECTED_AMOUNT = 100 # current amount is 0 + amount added

        self.assertEqual(self.wallet.amount, 0, "The current amount does not match with the expected amount")
        self.wallet.add_amount(AMOUNT_ADDED)
       
        self.bank_account.refresh_from_db()
        self.assertEqual(self.wallet.amount, EXPECTED_AMOUNT, "The current amount does not match with the expected amount")
    
    def test_deduct_amount(self):
        """Test if the amount is correctly deducted to the wallet"""

        wallet_id                       = "#1234567891112"
        EXPECTED_EXPECTED_AMOUNT_TO_ADD = 100
        AMOUNT_TO_DEDUCT                = 50
        EXPECTED_AMOUNT                 = 50


        bank_account = BankAccount.objects.create(bank_id="123456",
                                                 sort_code="100101",
                                                 account_number="01111101",
                                                 amount=EXPECTED_EXPECTED_AMOUNT_TO_ADD,
                                                 user=self.user
                                                         )
        
        wallet = Wallet.objects.create(
            wallet_id=wallet_id,
            user=self.user,
            bank_account=bank_account,
            amount=EXPECTED_EXPECTED_AMOUNT_TO_ADD,
        )
    
        wallet.refresh_from_db()
        self.assertEqual(wallet.amount, EXPECTED_EXPECTED_AMOUNT_TO_ADD)

        wallet.deduct_amount(AMOUNT_TO_DEDUCT)

        wallet.refresh_from_db()

        # Expected amount after deduction
        self.assertEqual(wallet.amount, EXPECTED_AMOUNT)

    def test_transfer_amount_from_wallet_to_bank(self):
        """Test that amount can be transferred from wallet to bank"""

        wallet_id                       = "#12345655555"
        EXPECTED_EXPECTED_AMOUNT_TO_ADD = 100
        AMOUNT_TO_TRANSFER              = 50
        EXPECTED_AMOUNT                 = 50

        bank_account = BankAccount.objects.create(bank_id="#1345678920",
                                                 sort_code="100102",
                                                 account_number="01111001",
                                                 user=self.user
                                                         )
        
        wallet = Wallet.objects.create(
            wallet_id=wallet_id,
            user=self.user,
            bank_account=bank_account,
            amount=EXPECTED_EXPECTED_AMOUNT_TO_ADD,
        )
        
        bank_account.refresh_from_db()
        wallet.refresh_from_db()

        # check that the bank amount before transfer is 0
        self.assertEqual(bank_account.amount, 0)

        # check that wallet has the expected funds before transfer
        self.assertEqual(wallet.amount, EXPECTED_EXPECTED_AMOUNT_TO_ADD)
        
        # Transfer amount to bank account
        TransferService.transfer_from_wallet_to_bank(bank_account, wallet, AMOUNT_TO_TRANSFER)

        # check if the amount has been transfered to the bank account and the wallet correctly updated
        bank_account.refresh_from_db()
        wallet.refresh_from_db()

        self.assertEqual(bank_account.amount, EXPECTED_AMOUNT)
        self.assertEqual(wallet.amount, EXPECTED_AMOUNT)

    def test_transfer_to_bank_raises_error_if_not_connected(self):
        """
        Ensure that transferring funds from a wallet to a bank account raises an error
        when the bank account is not connected.
        """

        wallet_id                       = "#19345655555"
        EXPECTED_EXPECTED_AMOUNT_TO_ADD = 100
        AMOUNT_TO_TRANSFER              = 50
      
        bank_account = BankAccount.objects.create(bank_id="#1345678920",
                                                 sort_code="100103",
                                                 account_number="01111000",
                                                 user=self.user
                                                         )
        
        wallet = Wallet.objects.create(
            wallet_id=wallet_id,
            user=self.user,
            amount=EXPECTED_EXPECTED_AMOUNT_TO_ADD,
        )
        

        # Test if error is raised
        with self.assertRaises(BankAccountIsNotConnectedToWalletError) as cm:
            TransferService.transfer_from_wallet_to_bank(bank_account, wallet, AMOUNT_TO_TRANSFER)
        
        exception_message = cm.exception
        expected_message  = "The bank account is not connected to the wallet"
        self.assertEqual(exception_message.message, expected_message )

    def test_get_wallet_by_wallet_id_method(self):
        """Test if the wallet can be retrieved using wallet id"""

        wallet = Wallet.get_by_wallet_id(self.wallet_id)
        self.assertIsInstance(wallet, Wallet)
    
    def test_get_wallet_by_bank_method(self):
        """Test if the wallet can be retrieved using the bank method"""

        wallet = Wallet.get_by_bank(self.bank_account)
        self.assertIsInstance(wallet, Wallet)

    def test_get_wallet_by_user_method(self):
        """Test if the wallet can be retrieved using the user method"""
        wallet = Wallet.get_by_user(self.user)
        self.assertIsInstance(wallet, Wallet)

