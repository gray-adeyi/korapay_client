from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class Response:
    status_code: int
    status: bool
    message: str
    data: dict | list | None


@dataclass
class Card:
    number: str
    cvv: str
    expiry_month: str
    expiry_year: str
    name: str | None = None
    pin: str | None = None


@dataclass
class AVS:
    state: str
    city: str
    country: str
    address: str
    zip_code: str


@dataclass
class Authorization:
    pin: str | None = None
    otp: str | None = None
    avs: AVS | None = None


@dataclass
class BankAccount:
    bank_code: str
    account_number: str


@dataclass
class Customer:
    email: str
    name: Optional[str] = None


@dataclass
class PayoutOrder:
    reference: str
    amount: int
    bank_account: BankAccount
    customer: Customer
    narration: Optional[str] = None
    type: Literal["bank_account", "mobile_money"] = "bank_account"
