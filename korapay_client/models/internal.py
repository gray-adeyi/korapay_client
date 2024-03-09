from typing import Any

from pydantic import BaseModel, EmailStr, field_validator, model_serializer, HttpUrl

from korapay_client.enums.public import Currency
from korapay_client.models.public import Card

MAX_METADATA_FIELDS = 5
MAX_METADATA_FIELD_KEY_CHAR = 20


class BaseMetadataModel(BaseModel):
    metadata: dict[str, Any] | None = None

    @field_validator("metadata")
    @classmethod
    def validate_metadata(cls, value: dict[str, Any]):
        if len(value.values()) > MAX_METADATA_FIELDS:
            raise ValueError("A maximum of 5 key/values is allowed")
        for key in value.keys():
            if len(key) > MAX_METADATA_FIELD_KEY_CHAR:
                raise ValueError(
                    "A metadata field key should not contain characters"
                    f" greater than {MAX_METADATA_FIELD_KEY_CHAR}"
                )
        return value


class ChargeViaCard(BaseMetadataModel):
    reference: str
    customer_name: str
    customer_email: EmailStr
    card: Card
    amount: int
    currency: Currency
    redirect_url: HttpUrl | None = None

    @model_serializer
    def serialize_self(self) -> dict[str, Any]:
        return {
            "reference": self.reference,
            "card": self.card.model_dump(exclude_none=True),
            "amount": self.amount,
            "currency": self.currency,
            "customer": {"name": self.customer_name, "email": self.customer_email},
        }
