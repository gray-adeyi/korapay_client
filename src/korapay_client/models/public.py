from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, Literal

from pydantic import BaseModel, EmailStr

from korapay_client.models.internal import SerializeAmountMixin


class Response(BaseModel):
    status_code: int
    status: bool
    message: str
    data: dict | list | None


@dataclass
class AVS(BaseModel):
    state: str
    city: str
    country: str
    address: str
    zip_code: str


class Authorization(BaseModel):
    pin: str | None = None
    otp: str | None = None
    avs: AVS | None = None


class BankAccount(BaseModel):
    bank_code: str
    account_number: str


class Customer(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class PayoutOrder(SerializeAmountMixin, BaseModel):
    reference: str
    amount: int | float | Decimal
    bank_account: BankAccount
    customer: Customer
    narration: Optional[str] = None
    type: Literal["bank_account", "mobile_money"] = "bank_account"
