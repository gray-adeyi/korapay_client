from typing import Type

from pydantic import BaseModel

from korapay_client.enums.internal import ClientMethod
from korapay_client.models.internal import (
    ChargeViaCardModel,
    ChargeViaBankTransferModel,
    CreateVirtualBankAccountModel,
    ChargeViaMobileMoneyModel,
    InitiateChargeModel,
)

client_methods_to_model_classes: dict[ClientMethod, Type[BaseModel]] = {
    ClientMethod.CHARGE_VIA_CARD: ChargeViaCardModel,
    ClientMethod.CHARGE_VIA_BANK_TRANSFER: ChargeViaBankTransferModel,
    ClientMethod.CREATE_VIRTUAL_BANK_ACCOUNT: CreateVirtualBankAccountModel,
    ClientMethod.CHARGE_VIA_MOBILE_MONEY: ChargeViaMobileMoneyModel,
    ClientMethod.INITIATE_CHARGE: InitiateChargeModel,
}


def get_validator_class(
    method: ClientMethod,
) -> Type[BaseModel]:
    model_class = client_methods_to_model_classes.get(method)
    if not model_class:
        raise NotImplementedError(
            f"A parameter validation model class for method: {method} "
            "has not been implemented or added to the `client_methods_to_model_classes` dict"
        )
    return model_class
