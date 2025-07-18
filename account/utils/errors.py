"""
Custom exceptions for user profile management.

This module defines a hierarchy of custom exceptions used throughout the user profile
handling system. All custom exceptions inherit from `CustomBaseError`, which provides a
consistent interface and message formatting across the application.

Classes:
    - CustomBaseError: The base class for all custom exceptions.
    - ProfileAlreadyExistsError: Raised when attempting to create a profile that already exists.
    - UserDoesNotExistError: Raised when operations are performed on a non-existent user.

Usage:
    These exceptions are intended to improve error handling clarity and provide more
    specific context when raising and catching errors in views, services, or forms.

Example:
    raise ProfileAlreadyExistsError()

    try:
        profile = Profile.get_by_user(user)
    except UserDoesNotExistError:
        handle_missing_user()



"""



class CustomBaseError(Exception):
    """
    Base class for custom application-specific exceptions.

    This class extends Python's built-in `Exception` class and provides a standard
    structure for all custom exceptions used in the application. It allows for a
    default message to be provided, and overrides the `__str__` method to return
    the message directly.

    Attributes:
        message (str): A human-readable error message. Defaults to "An error occurred."
    """
    def __init__(self, message=None):
        if message is None:
            message = "An error occurred."
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message




class ProfileAlreadyExistsError(CustomBaseError):
    """
    Raised when attempting to create a profile for a user who already has one.

    This exception is typically used to prevent duplicate profile creation,
    and to make sure that each user is associated with only one profile.

    Inherits from:
        CustomBaseError

    Default message:
        "A profile for this user already exists"
    """
    def __init__(self, message="A profile for this user already exists"):
        super().__init__(message)



class UserDoesNotExistError(CustomBaseError):
    """
    Raised when attempting to retrieve a user that does not exist.

    This exception is commonly used when retrieving or updating user-related data
    for a user that cannot be found in the system.

    Inherits from:
        CustomBaseError

    Default message:
        "The user doesn't exist"
    """
    def __init__(self, message="The user doesn't exist"):
        super().__init__(message)


class WalletInsufficientFundsError(CustomBaseError):
    """
    Raised when an operation attempts to withdraw or transfer more funds 
    than are available in the wallet.

    This exception is typically used in transaction-related logic where 
    the user's wallet balance is checked before proceeding.

    Inherits from:
        CustomBaseError

    Default message:
        "The wallet has insufficient funds"
    """
    def __init__(self, message="The wallet has insufficient funds"):
        super().__init__(message)



class BankInsufficientFundsError(CustomBaseError):
    """
    Raised when an operation attempts to withdraw or transfer more funds 
    than are available in the bank account.

    This exception is typically used in transaction-related logic where 
    the user's bank balance is checked before proceeding.

    Inherits from:
        CustomBaseError

    Default message:
        "The bank account has insufficient funds"
    """
    def __init__(self, message="The bank account has insufficient funds"):
        super().__init__(message)


class BankAccountIsNotConnectedToWalletError(CustomBaseError):
    """
    Raised when an operation attempts to withdraw or transfer funds 
    from a bank account that is not connected to the wallet

    This exception is typically used in transaction-related logic where 
    the user's bank balance is not connected to their wallet.

    Inherits from:
        CustomBaseError

    Default message:
        "The bank account is not connected to the wallet"
    """
    def __init__(self, message="The bank account is not connected to the wallet"):
        super().__init__(message)

class IncorrectBankTypeError(CustomBaseError):
    """
    Raised when an object that is not an instance of the expected BankAccount type 
    is used in a context requiring a valid bank account.

    Typically occurs when validating transaction inputs or initialising
    bank-related operations that require a BankAccount instance.

    Inherits from:
        CustomBaseError

    Default message:
        "Expected a BankAccount instance"
    """
    def __init__(self, message="Expected a BankAccount instance"):
        super().__init__(message)



class IncorrectWalletTypeError(CustomBaseError):
    """
    Raised when an object that is not an instance of the expected Wallet type 
    is used in a context requiring a valid wallet.

    Typically occurs during transaction handling or wallet initialisation 
    when a Wallet instance is required.

    Inherits from:
        CustomBaseError

    Default message:
        "Expected a Wallet instance"
    """
    def __init__(self, message="Expected a Wallet instance"):
        super().__init__(message)



class WalletCardLimitExceededError(CustomBaseError):
    """
    Raised when the number of cards in a Wallet exceeds the allowed maximum limit.

    This error typically occurs during transaction processing or wallet initialization
    when enforcing the maximum number of cards a Wallet can hold.
    """

    def __init__(self, message="The wallet card limit has been exceeded"):
        super().__init__(message)
