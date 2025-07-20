
# -------------------------------------------------------------------
# utils.py  
#--------------------------------------------------------------------

import logging
from .generator import generate_code

class RightIndentedFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        
        # Add a custom indent to the beginning of the log message
        original_message = super().format(record)
        return f"    {original_message}"  # 4 spaces or any amout of space you want



def mask_number(number: str, mask_all: bool = False, mask_char: str ="*", total_length: int = 16, group_size: int = 4):
    """
    Masks a numeric string (e.g. card or account number) by replacing characters 
    with a specified masking character.

    This function is typically used to obscure sensitive information such as 
    card numbers or bank account details. It supports partial masking 
    (preserving the last four digits) or full masking. You can also define the 
    total output length, which enables you to mask a number to a longer or 
    shorter fake length. 

    For example, an 8-digit account number can be masked to appear as a 
    16-digit string using the `total_length` parameter.

    Args:
        number (str): The numeric string to be masked (digits only).
        mask_all (bool, optional): Whether to mask the entire number. Defaults to False.
        mask_char (str, optional): The character to use for masking. Defaults to '*'.
        total_length (int, optional): The total length of the output string. Defaults to 16.
        group_size (int, optional): The number of characters per group when spacing. Defaults to 4.

    Returns:
        str: The masked number, spaced in groups (e.g. '**** **** **** 1234').

    Raises:
        TypeError: If `number` is not a string, or `total_length` / `group_size` are not integers.
        ValueError: If the number contains non-digit characters.

    Examples:
        >>> mask_number("1234567890123456")
        '**** **** **** 3456'

        >>> mask_number("1234", mask_all=True)
        '****************'

        >>> mask_number("1234567812345678", group_size=4)
        '**** **** **** 5678'
    """
    
    if not isinstance(number, str):
        raise TypeError(f"The number must be a string. Expected str but got {type(number).__name__}")
    
    if not isinstance(total_length, int):
        raise TypeError(f"The total length value must be an integer. Expected integer but got {type(total_length).__name__}")
    
    if not isinstance(group_size, int):
        raise TypeError(f"The group size must be an integer. Expected integer but got {type(total_length).__name__}")
    
    number = number.replace(" ", "")  # clean spaces
    
    if not number.isdigit():
        raise ValueError("The number must contain only digits.")
    
    if len(number) < 4:
        # Too short to mask meaningfully
        return mask_char * total_length

    if mask_all:
        masked = mask_char * total_length
    else:
        last4 = number[-4:]
        masked = mask_char * (total_length - 4) + last4

    return ' '.join([masked[i:i+4] for i in range(0, len(masked), group_size)])
