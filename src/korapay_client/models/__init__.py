"""
Models help to keep related data compact and is used by `korapay_client` client methods to accept compact data
required to process a request to Korapay. All client methods in `korapay_client` all return a `Response` which
is also a model.
Models are pydantic models as the `korapay_client` uses `pydantic` internally for validation and data
representation.

The models package contains all the internal and public models used by `korapay_client` package.

Note:
    All public models can be imported directly from `korapay_client`.
    E.g.,
    ```python
    from korapay_client import Authorization, PayoutOrder
    # `Authorization` and `PayoutOrder` are both models and can be used in client methods requiring them.
    auth = Authorization(pin='1234')
    ```
    You can use this models as you would use `dataclasses` although it can do a lot more. `korapay_client`
    only requires you to use them for data representations
"""

# ruff: noqa: F401
from korapay_client.models.public import (
    Response,
    AVS,
    Authorization,
    BankAccount,
    Customer,
    PayoutOrder,
)
from korapay_client.models.internal import Card
