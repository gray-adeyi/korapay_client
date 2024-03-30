from decimal import Decimal
from typing import Any

from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    model_serializer,
    HttpUrl,
    SerializerFunctionWrapHandler,
    field_serializer,
)

from korapay_client.enums.public import Currency, PaymentChannel
from korapay_client.models.public import Card

MAX_METADATA_FIELDS = 5
MAX_METADATA_FIELD_KEY_CHAR = 20


class SerializeAmountMixin:
    @field_serializer("amount")
    def serialize_amount(
        self, amount: int | float | Decimal, _info
    ) -> int | float | str:
        if isinstance(amount, Decimal):
            return str(amount)
        return amount


class MetadataValidationMixin:
    @field_validator("metadata")
    @classmethod
    def validate_metadata(cls, value: dict[str, Any] | None) -> dict[str, Any] | None:
        if not value:
            return None
        if len(value.values()) > MAX_METADATA_FIELDS:
            raise ValueError("A maximum of 5 key/values is allowed")
        for key in value.keys():
            if len(key) > MAX_METADATA_FIELD_KEY_CHAR:
                raise ValueError(
                    "A metadata field key should not contain characters"
                    f" greater than {MAX_METADATA_FIELD_KEY_CHAR}"
                )
        return value


class ChargeViaCardModel(MetadataValidationMixin, BaseModel):
    reference: str
    customer_name: str
    customer_email: EmailStr
    card: Card
    amount: int
    currency: Currency
    redirect_url: HttpUrl | None = None
    metadata: dict[str, Any] | None = None

    @model_serializer
    def serialize_self(self) -> dict[str, Any]:
        return {
            "reference": self.reference,
            "card": self.card,
            "amount": self.amount,
            "currency": self.currency,
            "customer": {"name": self.customer_name, "email": self.customer_email},
            "redirect_url": self.redirect_url,
            "meta": self.metadata,
        }


class ChargeViaBankTransferModel(MetadataValidationMixin, BaseModel):
    reference: str
    customer_email: str
    amount: int
    currency: Currency
    customer_name: str | None = None
    account_name: str | None = None
    narration: str | None = None
    notification_url: str | None = None
    merchant_bears_cost: bool = False
    metadata: dict[str, Any] | None = None

    @model_serializer(mode="wrap")
    def serialize_model(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        data = handler(self)
        customer_name = data.pop("customer_name", None)
        customer_email = data.pop("customer_email", None)
        if any([customer_name, customer_email]):
            data["customer"] = {}
            if customer_name:
                data["customer"]["name"] = customer_name
            if customer_email:
                data["customer"]["email"] = customer_email
        return data


class CreateVirtualBankAccountModel(BaseModel):
    account_name: str
    account_reference: str
    bank_code: str
    customer_name: str
    bvn: str
    customer_email: str | None = None
    nin: str | None = None
    permanent: bool = True

    @model_serializer(mode="wrap")
    def serialize_model(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        data = handler(self)
        customer_name = data.pop("customer_name")
        customer_email = data.pop("customer_email", None)
        bvn = data.pop("bvn")
        nin = data.pop("nin", None)
        data["customer"] = {"name": customer_name}
        if customer_email:
            data["customer"]["email"] = customer_email
        data["kyc"] = {"bvn": bvn}
        if nin:
            data["kyc"]["nin"] = nin
        return data


class ChargeViaMobileMoneyModel(MetadataValidationMixin, BaseModel):
    reference: str
    customer_email: str
    amount: int
    mobile_money_number: str
    currency: Currency
    notification_url: str | None = None
    customer_name: str | None = None
    redirect_url: str | None = None
    merchant_bears_cost: bool = False
    description: str | None = None
    metadata: dict[str, Any] | None = None

    @model_serializer(mode="wrap")
    def serialize_model(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        data = handler(self)
        mobile_money_number = data.pop("mobile_money_number")
        customer_email = data.pop("customer_email")
        customer_name = data.pop("customer_name", None)
        data["mobile_money"] = {"number": mobile_money_number}
        data["customer"] = {"email": customer_email}
        if customer_name:
            data["customer"]["name"] = customer_name
        return data


class InitiateChargeModel(SerializeAmountMixin, BaseModel):
    reference: str
    amount: int | float | Decimal
    currency: Currency
    narration: str
    notification_url: str
    customer_email: str
    customer_name: str | None = None
    channels: list[PaymentChannel] | None = None
    default_channel: PaymentChannel | None = None
    redirect_url: str | None = None

    @model_serializer(mode="wrap")
    def serialize_model(self, handler: SerializerFunctionWrapHandler) -> dict[str, Any]:
        data = handler(self)
        customer_email = data.pop("customer_email")
        customer_name = data.pop("customer_name", None)
        data["customer"] = {"email": customer_email}
        if customer_name:
            data["customer"]["name"] = customer_name
        return data
