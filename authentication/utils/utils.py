from django.http import HttpRequest
from django.urls import reverse


def create_verification_url(request: HttpRequest, username: str, url_name: str = "verify_registration_code") -> str:
    """
    Builds an absolute verification URL for the given username using the specified URL pattern name.

    Args:
        request (HttpRequest): The incoming HTTP request.
        username (str): The username to include in the URL.
        url_name (str): The name of the URL pattern to reverse (default: 'verify_registration_code').

    Returns:
        str: The full absolute verification URL.

    Raises:
        ValueError: If input types are incorrect.
        NoReverseMatch: If the URL name or arguments are invalid.
    """
    if not isinstance(request, HttpRequest):
        raise ValueError(f"Expected request to be HttpRequest, got {type(request)}")

    if not isinstance(username, str):
        raise ValueError(f"Expected username to be str, got {type(username)}")

    if not isinstance(url_name, str):
        raise ValueError(f"Expected url_name to be str, got {type(url_name)}")

    relative_url = reverse(url_name, args=[username])
    return request.build_absolute_uri(relative_url)