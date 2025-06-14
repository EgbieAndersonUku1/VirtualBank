from random import randint


def generate_code(maximum_length: int = 9) -> str:
    """
    Generates a random string based digit code based on the length provided.
    
    The function takes a `maximum_length` integer parameter and generates a 
    code based on the length provided. The code returned is a string of digits 
    (e.g '0525....5').
    
    Args:
        maximum_length (int): The maximum length to generate
        
    Example usage:
    
    >>> generate_code(9)
    '012345678'
    
    """
    code = "".join([str(_get_random_number()) for _ in range(maximum_length)])
    return code


def _get_random_number(start_number: int = 0, end_number: int = 9):
    """
    Takes a starting and ending number and generates an integer between
    and including the start and end number.
    """
    return randint(start_number, end_number)