from decimal import Decimal

from korapay_client.models import (
    Card,
    Response,
    Authorization,
    PayoutOrder,
)
from korapay_client.base_clients import AsyncBaseClient
from pydantic import EmailStr, HttpUrl

from korapay_client.clients.client_method_parameter_validator import get_validator_class
from korapay_client.enums import (
    ClientMethod,
    HTTPMethod,
    Currency,
    PaymentChannel,
    Country,
    MobileMoneyOperator,
)
from korapay_client.utils import encrypt_aes256


class AsyncKorapayClient(AsyncBaseClient):
    async def charge_via_card(
        self,
        reference: str,
        customer_name: str,
        customer_email: EmailStr,
        card: Card,
        amount: int | float | Decimal,
        currency: Currency,
        redirect_url: HttpUrl | None = None,
        metadata: dict | None = None,
    ) -> Response:
        parameter_validator_class = get_validator_class(ClientMethod.CHARGE_VIA_CARD)
        parameter_model = parameter_validator_class.model_validate(
            {
                "reference": reference,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "card": card,
                "amount": amount,
                "currency": currency,
                "redirect_url": redirect_url,
                "metadata": metadata,
            }
        )
        payload = parameter_model.model_dump(exclude_none=True)
        charge_data = encrypt_aes256(self._encryption_key, payload)
        return await self._process_request(
            endpoint="/merchant/api/v1/charges/card",
            method=HTTPMethod.POST,
            data={"charge_data": charge_data},
        )

    async def authorize_card_charge(
        self, transaction_reference: str, authorization: Authorization
    ) -> Response:
        data = {
            "transaction_reference": transaction_reference,
            "authorization": authorization.model_dump(exclude_none=True),
        }
        return await self._process_request(
            endpoint="/merchant/api/v1/charges/card/authorize",
            method=HTTPMethod.POST,
            data=data,
        )

    async def resend_card_otp(self, transaction_reference: str) -> Response:
        return await self._process_request(
            endpoint="/merchant/api/v1/charges/card/resend-otp",
            method=HTTPMethod.POST,
            data={"transaction_reference": transaction_reference},
        )

    async def charge_via_bank_transfer(
        self,
        reference: str,
        customer_email: str,
        amount: int | float | Decimal,
        currency: Currency,
        customer_name: str | None = None,
        account_name: str | None = None,
        narration: str | None = None,
        notification_url: str | None = None,
        merchant_bears_cost: bool = False,
        metadata: dict | None = None,
    ) -> Response:
        parameter_validator_class = get_validator_class(
            ClientMethod.CHARGE_VIA_BANK_TRANSFER
        )
        parameter_model = parameter_validator_class.model_validate(
            {
                "reference": reference,
                "amount": amount,
                "currency": currency,
                "notification_url": notification_url,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "account_name": account_name,
                "merchant_bears_cost": merchant_bears_cost,
                "narration": narration,
                "metadata": metadata,
            }
        )
        data = parameter_model.model_dump(exclude_none=True)
        return await self._process_request(
            endpoint="/merchant/api/v1/charges/bank-transfer",
            method=HTTPMethod.POST,
            data=data,
        )

    async def create_virtual_bank_account(
        self,
        account_name: str,
        account_reference: str,
        bank_code: str,
        customer_name: str,
        bvn: str,
        customer_email: str | None = None,
        nin: str | None = None,
    ) -> Response:
        parameter_validator_class = get_validator_class(
            ClientMethod.CREATE_VIRTUAL_BANK_ACCOUNT
        )
        parameter_model = parameter_validator_class.model_validate(
            {
                "account_name": account_name,
                "account_reference": account_reference,
                "bank_code": bank_code,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "bvn": bvn,
                "nin": nin,
            }
        )
        data = parameter_model.model_dump(exclude_none=True)
        return await self._process_request(
            endpoint="/merchant/api/v1/virtual-bank-account",
            method=HTTPMethod.POST,
            data=data,
        )

    async def get_virtual_bank_account(self, account_reference: str) -> Response:
        return await self._process_request(
            endpoint=f"/merchant/api/v1/virtual-bank-account/{account_reference}",
            method=HTTPMethod.GET,
        )

    async def get_virtual_bank_account_transactions(
        self, account_number: str
    ) -> Response:
        return await self._process_request(
            endpoint=f"/merchant/api/v1/virtual-bank-account/transactions?account_number={account_number}",
            method=HTTPMethod.GET,
        )

    async def credit_sandbox_virtual_bank_account(
        self, account_number: str, amount: int | float | Decimal, currency: Currency
    ) -> Response:
        data = {
            "account_number": account_number,
            "amount": amount,
            "currency": currency.value,
        }
        return await self._process_request(
            endpoint="/merchant/api/v1/virtual-bank-account/sandbox/credit",
            method=HTTPMethod.POST,
            data=data,
        )

    async def charge_via_mobile_money(
        self,
        reference: str,
        customer_email: str,
        amount: int | float | Decimal,
        mobile_money_number: str,
        currency: Currency,
        notification_url: str | None = None,
        customer_name: str | None = None,
        redirect_url: str | None = None,
        merchant_bears_cost: bool = False,
        description: str | None = None,
        metadata: dict | None = None,
    ) -> Response:
        parameter_validator_class = get_validator_class(
            ClientMethod.CHARGE_VIA_MOBILE_MONEY
        )
        parameter_model = parameter_validator_class.model_validate(
            {
                "reference": reference,
                "amount": amount,
                "currency": currency.value,
                "redirect_url": redirect_url,
                "customer_email": customer_email,
                "customer_name": customer_name,
                "mobile_money_number": mobile_money_number,
                "notification_url": notification_url,
                "merchant_bears_cost": merchant_bears_cost,
                "description": description,
                "metadata": metadata,
            }
        )
        data = parameter_model.model_dump(exclude_none=True)
        return await self._process_request(
            endpoint="/merchant/api/v1/charges/mobile-money",
            method=HTTPMethod.POST,
            data=data,
        )

    async def authorize_mobile_money_charge(
        self, reference: str, token: str
    ) -> Response:
        return await self._process_request(
            endpoint="/merchant/api/v1/charges/mobile-money/authorize",
            method=HTTPMethod.POST,
            data={
                "reference": reference,
                "token": token,
            },
        )

    async def resend_mobile_money_otp(self, transaction_reference: str) -> Response:
        return await self._process_request(
            endpoint="/merchant/api/v1/charges/mobile-money/resend-otp",
            method=HTTPMethod.POST,
            data={"transaction_reference": transaction_reference},
        )

    async def resend_stk(self, transaction_reference: str) -> Response:
        return await self._process_request(
            endpoint="/merchant/api/v1/charges/mobile-money/resend-stk",
            method=HTTPMethod.POST,
            data={"transaction_reference": transaction_reference},
        )

    async def authorize_stk(self, reference: str, pin: str) -> Response:
        return await self._process_request(
            endpoint="/merchant/api/v1/charges/mobile-money/sandbox/authorize-stk",
            method=HTTPMethod.POST,
            data={"reference": reference, "pin": pin},
        )

    async def initiate_charge(
        self,
        reference: str,
        amount: int | float | Decimal,
        currency: Currency,
        narration: str,
        notification_url: str,
        customer_email: str,
        customer_name: str | None = None,
        channels: list[PaymentChannel] | None = None,
        default_channel: PaymentChannel | None = None,
        redirect_url: str | None = None,
    ) -> Response:
        parameter_validator_class = get_validator_class(ClientMethod.INITIATE_CHARGE)
        parameter_model = parameter_validator_class.model_validate(
            {
                "reference": reference,
                "amount": amount,
                "currency": currency,
                "narration": narration,
                "notification_url": notification_url,
                "customer_email": customer_email,
                "customer_name": customer_name,
                "default_channel": default_channel,
                "redirect_url": redirect_url,
                "channels": channels,
            }
        )
        data = parameter_model.model_dump(exclude_none=True)
        return await self._process_request(
            endpoint="/merchant/api/v1/charges/initialize",
            method=HTTPMethod.POST,
            data=data,
        )

    async def get_charge(self, reference: str) -> Response:
        return await self._process_request(
            endpoint=f"/merchant/api/v1/charges/{reference}", method=HTTPMethod.GET
        )

    async def resolve_bank_account(
        self, bank_code: str, account_number: str
    ) -> Response:
        return await self._process_request(
            endpoint="/merchant/api/v1/misc/banks/resolve",
            method=HTTPMethod.POST,
            data={"bank": bank_code, "account": account_number},
        )

    async def get_balances(self) -> Response:
        return await self._process_request(
            endpoint="/merchant/api/v1/balances",
            method=HTTPMethod.GET,
        )

    async def get_banks(self, country: Country) -> Response:
        return await self._process_request(
            endpoint=f"/merchant/api/v1/misc/banks?countryCode={country.value}",
            method=HTTPMethod.GET,
            use_public_auth=True,
        )

    async def get_mmo(self, country: Country) -> Response:
        return await self._process_request(
            endpoint=f"/merchant/api/v1/misc/mobile-money?countryCode={country.value}",
            method=HTTPMethod.GET,
            use_public_auth=True,
        )

    async def payout_to_bank_account(
        self,
        reference: str,
        amount: int | float | Decimal,
        currency: Currency,
        bank_code: str,
        account_number: str,
        customer_email: str,
        narration: str | None = None,
        customer_name: str | None = None,
    ) -> Response:
        parameter_validator_class = get_validator_class(
            ClientMethod.PAYOUT_TO_BANK_ACCOUNT
        )
        parameter_model = parameter_validator_class.model_validate(
            {
                "reference": reference,
                "amount": amount,
                "currency": currency,
                "narration": narration,
                "bank_code": bank_code,
                "account_number": account_number,
                "customer_email": customer_email,
                "customer_name": customer_name,
            }
        )
        data = parameter_model.model_dump(exclude_none=True)
        return await self._process_request(
            endpoint="/merchant/api/v1/transactions/disburse",
            method=HTTPMethod.POST,
            data=data,
        )

    async def payout_to_mobile_money(
        self,
        reference: str,
        amount: int | float | Decimal,
        currency: Currency,
        mobile_money_operator: MobileMoneyOperator | str,
        mobile_number: str,
        customer_email: str,
        customer_name: str | None = None,
        narration: str | None = None,
    ) -> Response:
        parameter_validator_class = get_validator_class(
            ClientMethod.PAYOUT_TO_MOBILE_MONEY
        )
        parameter_model = parameter_validator_class.model_validate(
            {
                "reference": reference,
                "amount": amount,
                "currency": currency,
                "narration": narration,
                "mobile_money_operator": mobile_money_operator,
                "mobile_number": mobile_number,
                "customer_email": customer_email,
                "customer_name": customer_name,
            }
        )
        data = parameter_model.model_dump(exclude_none=True)
        return await self._process_request(
            endpoint="/merchant/api/v1/transactions/disburse",
            method=HTTPMethod.POST,
            data=data,
        )

    async def bulk_payout_to_bank_account(
        self,
        batch_reference: str,
        description: str,
        merchant_bears_cost: bool,
        currency: Currency,
        payouts: list[PayoutOrder],
    ) -> Response:
        data = {
            "batch_reference": batch_reference,
            "description": description,
            "merchant_bears_cost": merchant_bears_cost,
            "currency": currency.value,
            "payouts": [payout.model_dump(exclude_none=True) for payout in payouts],
        }
        return await self._process_request(
            endpoint="/api/v1/transactions/disburse/bulk",
            method=HTTPMethod.POST,
            data=data,
        )

    async def get_payouts(self, bulk_reference: str) -> Response:
        return await self._process_request(
            endpoint=f"/api/v1/transactions/bulk/{bulk_reference}/payout",
            method=HTTPMethod.GET,
        )

    async def get_bulk_transaction(self, bulk_reference: str) -> Response:
        return await self._process_request(
            endpoint=f"/api/v1/transactions/bulk/{bulk_reference}",
            method=HTTPMethod.GET,
        )

    async def verify_payout_transaction(self, transaction_reference: str) -> Response:
        return await self._process_request(
            endpoint=f"/merchant/api/v1/transactions/{transaction_reference}",
            method=HTTPMethod.GET,
        )
