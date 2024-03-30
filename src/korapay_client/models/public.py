from dataclasses import dataclass
from typing import Optional, Literal

from pydantic import BaseModel, EmailStr


class Response(BaseModel):
    status_code: int
    status: bool
    message: str
    data: dict | list | None


class Card(BaseModel):
    number: str
    cvv: str
    expiry_month: str
    expiry_year: str
    name: str | None = None
    pin: str | None = None


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


class PayoutOrder(BaseModel):
    reference: str
    amount: int
    bank_account: BankAccount
    customer: Customer
    narration: Optional[str] = None
    type: Literal["bank_account", "mobile_money"] = "bank_account"
