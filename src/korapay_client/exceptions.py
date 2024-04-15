class MissingAPIKeyError(Exception): ...


class UnsupportedHTTPMethodError(Exception): ...


class ClientError(Exception):
    """Raised when an error or exception occurs while making the request to Korapay."""

    ...
