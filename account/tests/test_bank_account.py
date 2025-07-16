from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from freezegun import freeze_time


from ..models import BankAccount, Wallet
from authentication.models import User
from ..utils.errors import BankInsufficientFundsError


# Create your tests here.

@freeze_time("2025-07-14 16:00:00")
class BankAccountTest(TestCase):

    def setUp(self):

        self.user           = User.objects.create(
                                first_name="Test name",
                                surname="Test surname",
                                username="Test username",
                                email="test@example.com",
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
  
    def test_creation_count(self):
        """Test if the bank account object was successfully created"""

        self.assertTrue(
            BankAccount.objects.filter(bank_id=self.bank_id).exists(),
            msg="Expected a bank account object"
        )
        self.assertEqual(
            BankAccount.objects.count(), 
            1, 
            msg="Expected a single creation count"
        )
    
    def test__str__model(self):
        expected_str = self.bank_account.full_account_number
        self.assertEqual(str(self.bank_account), expected_str)

    def test_username_property_returns_user_username(self):
        self.assertEqual(self.bank_account.username, self.user.username)

    def test_email_property_returns_user_email(self):
        self.assertEqual(self.bank_account.email, self.user.email)

    def test_full_account_number_property_returns_concatenated_sort_code_and_account_number(self):
        expected = f"{self.bank_account.sort_code}{self.bank_account.account_number}"
        self.assertEqual(self.bank_account.full_account_number, expected)

    def test_pin_property_returns_user_pin(self):
        self.assertEqual(self.bank_account.pin, self.user.pin)

    def test_bank_account_fields(self):
        """Test if the fields are save correctly in the database"""

        # refresh the model so it pulls from the database and not the saved instance
        self.bank_account.refresh_from_db()

        self.assertEqual(self.bank_account.bank_id, self.bank_id)
        self.assertEqual(self.bank_account.sort_code, self.sort_code)
        self.assertEqual(self.bank_account.account_number, self.account_number)
        self.assertEqual(self.bank_account.amount, self.amount)
        self.assertIsInstance(self.bank_account.user, User)

        # frozen time check
        frozen_time = timezone.now()

        self.assertEqual(self.bank_account.created_on, frozen_time)
        self.assertEqual(self.bank_account.modified_on, frozen_time)
    
    def test_add_amount(self):
        """Test if the amount is correctly add to the bank account"""

        # refresh the model so it pulls from the database and not the saved instance
        self.bank_account.refresh_from_db()

        AMOUNT_ADDED    = 100
        EXPECTED_AMOUNT = 200 # current amount is 100 + amount added

        self.assertEqual(self.bank_account.amount, self.amount, "The current amount does not match with the expected amount")
        self.bank_account.add_amount(AMOUNT_ADDED)
       
        self.bank_account.refresh_from_db()
        self.assertEqual(self.bank_account.amount, EXPECTED_AMOUNT, "The current amount does not match with the expected amount")
    
    def test_get_by_account_number_returns_correct_account(self):

        account = BankAccount.get_by_account_number(self.sort_code, self.account_number)
        self.assertEqual(account, self.bank_account)
        self.assertIsInstance(account, BankAccount)

    def test_get_by_account_number_returns_none_if_not_found(self):
        account = BankAccount.get_by_account_number("999999", "00000000")
        self.assertIsNone(account)
    
    def test_get_by_user_returns_correct_account(self):
        account = BankAccount.get_by_user(self.user)
        self.assertEqual(account, self.bank_account)
        self.assertIsInstance(account, BankAccount)

    def test_get_by_user_returns_none_if_no_account_exists(self):
        new_user = User.objects.create(
            first_name="Another", surname="Person", username="someoneelse",
            email="other@example.com", pin="5678"
        )
        account = BankAccount.get_by_user(new_user)
        self.assertIsNone(account)
    
    def test_amount_field_validator_disallows_negative_amount_directly(self):
        account = BankAccount(
            bank_id="XNEG123",
            sort_code="401111",
            account_number="99988877",
            amount=-10,  # invalid
            user=self.user
        )
        with self.assertRaises(ValidationError):
            account.full_clean()

    def test_unique_together_constraint_on_sort_code_and_account_number(self):
        with self.assertRaises(IntegrityError):
            BankAccount.objects.create(
                bank_id=self.bank_id,                # duplicated id
                sort_code=self.sort_code,
                account_number=self.account_number,  # same as self.bank_account
                amount=0,
                user=self.user
        )
            
    @freeze_time("2025-07-14 17:30:00")
    def test_modified_on_field_is_updated_after_save(self):
        bank_account = BankAccount.objects.create(
            bank_id="12345678",
            sort_code="400123",
            account_number="01215987",
            amount=100,
            user=self.user,
        )
        created_on = bank_account.created_on
        modified_on_initial = bank_account.modified_on

        self.assertEqual(created_on, modified_on_initial)

        # Advance time to simulate a delay
        with freeze_time("2025-07-14 17:30:10"):
            bank_account.amount += 50
            bank_account.save()
            bank_account.refresh_from_db()

            self.assertGreater(bank_account.modified_on, modified_on_initial)

    def test_deduct_amount(self):
        """Test if the amount is correctly add to the bank account"""

        AMOUNT_TO_ADD    = 50
        AMOUNT_TO_DEDUCT = 40
        EXPECTED_AMOUNT  = 10


        bank_account = BankAccount.objects.create(bank_id="12345678",
                                                  sort_code="400123",
                                                  account_number="01215987",
                                                  amount=AMOUNT_TO_ADD,
                                                  user=self.user
                                                         )

    
      
        self.assertEqual(bank_account.amount, AMOUNT_TO_ADD, "The current amount does not match with the expected amount")
        bank_account.deduct_amount(AMOUNT_TO_DEDUCT)
       
        # pull from the database and not the instance model
        bank_account.refresh_from_db()
        self.assertEqual(bank_account.amount, EXPECTED_AMOUNT, "The current amount does not match with the expected amount")
    
    
    def test_raises_error_when_withdrawing_more_than_balance(self):
        AMOUNT_TO_ADD    = 50
        AMOUNT_TO_DEDUCT = 100

        bank_account = BankAccount.objects.create(
            bank_id="123456781011",
            sort_code="400123",
            account_number="01215987",
            amount=AMOUNT_TO_ADD,
            user=self.user
        )

        self.assertEqual(
            bank_account.amount,
            AMOUNT_TO_ADD,
            "Expected the amount to match the initial deposit"
        )

        with self.assertRaises(BankInsufficientFundsError) as cm:
            bank_account.deduct_amount(AMOUNT_TO_DEDUCT)

        overdrawn = bank_account.amount - AMOUNT_TO_DEDUCT
        expected_message = (
            f"Insufficient amount for withdrawal, current amount: {bank_account.amount}, "
            f"withdrawal amount: {AMOUNT_TO_DEDUCT}, overdrawn: {overdrawn}"
        )

        the_exception = cm.exception
        self.assertEqual(str(the_exception), expected_message)
