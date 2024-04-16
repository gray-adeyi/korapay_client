from enum import Enum


class MobileMoneyOperator(str, Enum):
    """An enum of mobile money operators supported by Korapay.

    Attributes:
        SAFARICOM_KENYA (str): an enum variant.
        AIRTEL_KENYA (str): an enum variant.
        AIRTEL_GHANA (str): an enum variant.
        MTN_GHANA (str): an enum variant.

    Example:
        ```python
        from korapay_client import MobileMoneyOperator
        mmo = MobileMoneyOperator.AIRTEL_KENYA
        ```

    Note:
        Some client methods might require this enum as a parameter. Use the variant
        of this enum that aligns with your needs.
    """

    SAFARICOM_KENYA = "safaricom-ke"
    AIRTEL_KENYA = "airtel-ke"
    AIRTEL_GHANA = "airtel-gh"
    MTN_GHANA = "mtn-gh"


class Currency(str, Enum):
    """An enum of currencies supported by Korapay.

    Attributes:
        NGN (str): an enum variant.
        KES (str): an enum variant.
        GHS (str): an enum variant.
        USD (str): an enum variant.

    Example:
        ```python
        from korapay_client import Currency
        ngn = Currency.NGN
        ghs = Currency.GHS
        ```

    Note:
        Some client methods might require this enum as a parameter. Use the variant
        of this enum that aligns with your needs.
    """

    NGN = "NGN"
    KES = "KES"
    GHS = "GHS"
    USD = "USD"


class PaymentChannel(str, Enum):
    """An enum of payment channels supported by Korapay.

    Attributes:
        CARD (str): an enum variant.
        BANK_TRANSFER (str): an enum variant.
        MOBILE_MONEY (str): an enum variant.

    Example:
        ```python
        from korapay_client import PaymentChannel
        channel = PaymentChannel.BANK_TRANSFER
        ```

    Note:
        Some client methods might require this enum as a parameter. Use the variant
        of this enum that aligns with your needs.
    """

    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    MOBILE_MONEY = "mobile_money"


class Country(str, Enum):
    """An enums of countries supported by Korapay.

    Attributes:
        NIGERIA (str): an enum variant.
        KENYA (str): an enum variant.
        GHANA (str): an enum variant.

    Example:
        ```python
        from korapay_client import Country
        ng = Country.NIGERIA
        ```

    Note:
        Some client methods might require this enum as a parameter. Use the variant
        of this enum that aligns with your needs.
    """

    NIGERIA = "NG"
    KENYA = "KE"
    GHANA = "GH"
