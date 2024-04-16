class MissingAPIKeyError(Exception):
    """Raised when any of the public key, secret key and encryption key is missing"""

    ...


class UnsupportedHTTPMethodError(Exception): ...


class ClientError(Exception):
    """Raised when an error or exception occurs while making the request to Korapay."""

    ...
