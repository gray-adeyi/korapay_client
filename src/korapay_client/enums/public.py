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
