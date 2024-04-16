"""
Enumerations help improve developer experience as it limits the number of options available for a parameter value.

The enums package contains all the internal and public enums used by `korapay_client` package.

Note:
    All public enums can be imported directly from `korapay_client`.
    E.g.,
    ```python
    from korapay_client import Currency, Country
    # `Currency` and `Country` are both enums and can be used in client methods requiring them
    nigeria = Country.NIGERIA
    currency = Currency.NGN
    ```
"""

# ruff: noqa: F401
from korapay_client.enums.internal import HTTPMethod, ClientMethod
from korapay_client.enums.public import (
    MobileMoneyOperator,
    Currency,
    PaymentChannel,
    Country,
)
