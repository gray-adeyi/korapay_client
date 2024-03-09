from enum import Enum


class Currency(str, Enum):
    NGN = "NGN"
    KES = "KES"
    GHS = "GHS"
    USD = "USD"


class PaymentChannel(str, Enum):
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    MOBILE_MONEY = "mobile_money"


class Country(str, Enum):
    NIGERIA = "NG"
    KENYA = "KE"
    GHANA = "GH"


class HTTPMethod(str, Enum):
    """An enum of supported HTTP verbs."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
