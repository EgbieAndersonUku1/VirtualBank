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
