from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Literal

from pydantic import BaseModel, EmailStr

from korapay_client.models.internal import SerializeAmountMixin


class Response(BaseModel):
    """A pydantic model for representing the response returned from making a request to Korapay
    by calling any of the client methods.

    This model is the return type of all client methods that make REST API calls to Korapay.

    Attributes:
        status_code: The HTTP status code of the response.
        status: The status of the response.
        message: The message of the response.
        data: The data returned by Korapay as a result of making the request.

    Example:
        ```python
        from korapay import KorapayClient, Country
        client = KorapayClient() # assumes the credentials are in the environmental variables
        response = client.get_banks(country=Country.NIGERIA)
        print(response.status_code)
        print(response.data)
        print(response)
        ```
    """

    status_code: int
    status: bool
    message: str
    data: dict | list | None


@dataclass
class AVS(BaseModel):
    """A pydantic model for representing the address information of a debit card for
    Address Verification Service.

    Attributes:
        state: The state of the customer.
        city: The city of the customer.
        country: The country of the customer.
        address: The address of the customer.
        zip_code: The zip code of the customer.

    Example:
        ```python
        from korapay_client import AVS, Country
        avs = AVS(state='lagos',city='alimosho',
        country=Country.NIGERIA.value,address='404 anonymous street',zip_code='253359')
        # OR
        data = {
            'state': 'lagos',
            'city':'alimosho',
            'country':'NG',
            'address':'404 anonymous street',
            'zip_code':'253359'
        }
        avs = AVS.model_validate(data)
        ```
    """

    state: str
    city: str
    country: str
    address: str
    zip_code: str


class Authorization(BaseModel):
    """A pydantic model for representing additional information required by Korapay for
    authorizing a charge on the card.

    Attributes:
        pin: The debit card pin of the customer.
        otp: The one time password/pin obtained from the customer.
        avs: The AVS of the customer

    Example:
        ```python
        from korapay_client import Authorization
        auth = Authorization(pin='1234')
        ```

    Note:
        For the different authorization flow, you'll only need to provide one of the fields
    """

    pin: str | None = None
    otp: str | None = None
    avs: AVS | None = None


class BankAccount(BaseModel):
    """A pydantic model for representing bank account information.

    Attributes:
        bank_code: The code representing the bank e.g., 035.
        account_number: The account number of the customer.

    Example:
        ```python
        from korapay_client import BankAccount
        account = BankAccount(bank_code='033', account_number='0000000000')
        ```
    """

    bank_code: str
    account_number: str


class Customer(BaseModel):
    """A pydantic model for representing customer's information.

    Attributes:
        email: The email address of the customer.
        name: The name of the customer.

    Example:
        ```python
        from korapay_client import Customer
        cus = Customer(email='johndoe@example.com', name='John Doe')
        ```
    """

    email: EmailStr
    name: Optional[str] = None


class PayoutOrder(SerializeAmountMixin, BaseModel):
    """A pydantic model for representing individual transactions in a bulk payout.

    Attributes:
        reference: The reference of the transaction.
        amount: The amount to pay the recipient.
        bank_account: The bank account information of the recipient.
        customer: The information about the recipient.
        narration: The description of the transaction.
        type: The payment channel of the payout. defaults to `bank_account`
            as it is the only payout payment channel supported by Korapay.

    Example:
        ```python
        from korapay_client import PayoutOrder
        data = {
            'reference': 'qqwerefdvifogirfguitheopwe',
            'amount' 100_000,
            'bank_account': {'bank_code':'033', 'account_number': '0000000000'},
            'customer': {'email': 'johndoe@example.com' , 'name': 'John Doe'},
            'narration': 'A test payout',
            }
        payout_order = PayoutOrder.model_validate(data)
        ```
    """

    reference: str
    amount: int | float | Decimal
    bank_account: BankAccount
    customer: Customer
    narration: Optional[str] = None
    type: Literal["bank_account", "mobile_money"] = "bank_account"
