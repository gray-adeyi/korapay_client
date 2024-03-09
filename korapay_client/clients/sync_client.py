from dataclasses import asdict

from korapay_client.base_clients import BaseClient
from korapay_client.enums import Currency, PaymentChannel, Country, HTTPMethod
from korapay_client.models import Authorization, Card, Response, PayoutOrder
from korapay_client.utils import encrypt_aes256, validate_metadata


class KorapayClient(BaseClient):
    def charge_via_card(
        self,
        reference: str,
        customer_name: str,
        customer_email: str,
        card: Card,
        amount: int,
        currency: Currency,
        redirect_url: str | None = None,
        metadata: dict | None = None,
    ) -> Response:
        payload = {
            "reference": reference,
            "card": asdict(card),
            "amount": amount,
            "currency": currency.value,
            "customer": {"name": customer_name, "email": customer_email},
        }
        if redirect_url:
            payload["redirect_url"] = redirect_url
        if metadata:
            validate_metadata(metadata)
            payload["metadata"] = metadata

        charge_data = encrypt_aes256(self._encryption_key, payload)
        return self._process_request(
            endpoint="/merchant/api/v1/charges/card",
            method=HTTPMethod.POST,
            data={"charge_data": charge_data},
        )

    def authorize_card_charge(
        self, transaction_reference: str, authorization: Authorization
    ) -> Response:
        data = {
            "transaction_reference": transaction_reference,
            "authorization": asdict(authorization),
        }
        return self._process_request(
            endpoint="/merchant/api/v1/charges/card/authorize",
            method=HTTPMethod.POST,
            data=data,
        )

    def resend_card_otp(self, transaction_reference: str) -> Response:
        return self._process_request(
            endpoint="/merchant/api/v1/charges/card/resend-otp",
            method=HTTPMethod.POST,
            data={"transaction_reference": transaction_reference},
        )

    def charge_via_bank_transfer(
        self,
        reference: str,
        customer_email: str,
        amount: int,
        currency: Currency,
        customer_name: str | None = None,
        account_name: str | None = None,
        narration: str | None = None,
        notification_url: str | None = None,
        merchant_bears_cost: bool = False,
        metadata: dict | None = None,
        autocomplete: bool = False,
    ) -> Response:
        data = {
            "reference": reference,
            "amount": amount,
            "currency": currency.value,
            "notification_url": notification_url,
            "customer": {"name": customer_name, "email": customer_email},
            "account_name": account_name,
            "merchant_bears_cost": merchant_bears_cost,
            "narration": narration,
            "autocomplete": autocomplete,
        }
        if metadata:
            validate_metadata(metadata)
            data["metadata"] = metadata
        return self._process_request(
            endpoint="/merchant/api/v1/charges/bank-transfer",
            method=HTTPMethod.POST,
            data=data,
        )

    def create_virtual_bank_account(
        self,
        account_name: str,
        account_reference: str,
        bank_code: str,
        customer_name: str,
        bvn: str,
        customer_email: str | None = None,
        nin: str | None = None,
    ) -> Response:
        data = {
            "account_name": account_name,
            "account_reference": account_reference,
            "permanent": True,
            "bank_code": bank_code,
            "customer": {"name": customer_name, "email": customer_email},
            "kyc": {"bvn": bvn, "nin": nin},
        }
        return self._process_request(
            endpoint="/merchant/api/v1/virtual-bank-account",
            method=HTTPMethod.POST,
            data=data,
        )

    def get_virtual_bank_account(self, account_reference: str) -> Response:
        return self._process_request(
            endpoint=f"/merchant/api/v1/virtual-bank-account/{account_reference}",
            method=HTTPMethod.GET,
        )

    def get_virtual_bank_account_transactions(self, account_number: str) -> Response:
        return self._process_request(
            endpoint=f"/merchant/api/v1/virtual-bank-account/transactions?account_number={account_number}",
            method=HTTPMethod.GET,
        )

    def credit_sandbox_virtual_bank_account(
        self, account_number: str, amount: int, currency: Currency
    ) -> Response:
        data = {
            "account_number": account_number,
            "amount": amount,
            "currency": currency.value,
        }
        return self._process_request(
            endpoint="/merchant/api/v1/virtual-bank-account/sandbox/credit",
            method=HTTPMethod.POST,
            data=data,
        )

    def charge_via_mobile_money(
        self,
        reference: str,
        customer_email: str,
        amount: int,
        mobile_money_number: str,
        currency: Currency,
        notification_url: str | None = None,
        customer_name: str | None = None,
        redirect_url: str | None = None,
        merchant_bears_cost: bool = False,
        description: str | None = None,
        metadata: dict | None = None,
    ) -> Response:
        data = {
            "reference": reference,
            "amount": amount,
            "currency": currency.value,
            "redirect_url": redirect_url,
            "customer": {"email": customer_email, "name": customer_name},
            "mobile_money": {"number": mobile_money_number},
            "notification_url": notification_url,
            "merchant_bears_cost": merchant_bears_cost,
            "description": description,
        }
        if metadata:
            validate_metadata(metadata)
            data["metadata"] = metadata
        return self._process_request(
            endpoint="/merchant/api/v1/charges/mobile-money",
            method=HTTPMethod.POST,
            data=data,
        )

    def authorize_mobile_money_charge(self, reference: str, token: str) -> Response:
        return self._process_request(
            endpoint="/merchant/api/v1/charges/mobile-money/authorize",
            method=HTTPMethod.POST,
            data={"reference": reference, "token": token},
        )

    def resend_mobile_money_otp(self, transaction_reference: str) -> Response:
        return self._process_request(
            endpoint="/merchant/api/v1/charges/mobile-money/resend-otp",
            method=HTTPMethod.POST,
            data={"transaction_reference": transaction_reference},
        )

    def resend_stk(self, transaction_reference: str) -> Response:
        return self._process_request(
            endpoint="/merchant/api/v1/charges/mobile-money/resend-stk",
            method=HTTPMethod.POST,
            data={"transaction_reference": transaction_reference},
        )

    def authorize_stk(self, reference: str, pin: str) -> Response:
        return self._process_request(
            endpoint="/merchant/api/v1/charges/mobile-money/sandbox/authorize-stk",
            method=HTTPMethod.POST,
            data={"reference": reference, "pin": pin},
        )

    def initiate_charge(
        self,
        reference: str,
        amount: int,
        currency: Currency,
        narration: str,
        notification_url: str,
        customer_email: str,
        customer_name: str | None = None,
        channels: list[PaymentChannel] | None = None,
        default_channel: PaymentChannel | None = None,
        redirect_url: str | None = None,
    ) -> Response:
        data = {
            "reference": reference,
            "amount": amount,
            "currency": currency.value,
            "narration": narration,
            "notification_url": notification_url,
            "customer": {"email": customer_email, "name": customer_name},
            "default_channel": default_channel.value,
            "redirect_url": redirect_url,
        }
        if channels:
            data["channels"] = [channel.value for channel in channels]
        return self._process_request(
            endpoint="/merchant/api/v1/charges/initialize",
            method=HTTPMethod.POST,
            data=data,
        )

    def get_charge(self, reference: str) -> Response:
        return self._process_request(
            endpoint=f"/merchant/api/v1/charges/{reference}", method=HTTPMethod.GET
        )

    def resolve_bank_account(self, bank_code: str, account_number: str) -> Response:
        return self._process_request(
            endpoint="/merchant/api/v1/misc/banks/resolve",
            method=HTTPMethod.POST,
            data={"bank": bank_code, "account": account_number},
        )

    def get_balances(self) -> Response:
        return self._process_request(
            endpoint="/merchant/api/v1/balances",
            method=HTTPMethod.GET,
        )

    def get_banks(self, country: Country) -> Response:
        return self._process_request(
            endpoint=f"/merchant/api/v1/misc/banks?countryCode={country.value}",
            method=HTTPMethod.GET,
        )

    def get_mmo(self, country: Country) -> Response:
        return self._process_request(
            endpoint=f"/merchant/api/v1/misc/mobile-money?countryCode={country.value}",
            method=HTTPMethod.GET,
        )

    def payout_to_bank_account(
        self,
        reference: str,
        amount: int,
        currency: Currency,
        bank_code: str,
        account_number: str,
        customer_email: str,
        narration: str | None = None,
        customer_name: str | None = None,
    ) -> Response:
        data = {
            "reference": reference,
            "destination": {
                "type": "bank_account",
                "amount": amount,
                "currency": currency.value,
                "narration": narration,
                "bank_account": {"bank": bank_code, "account": account_number},
                "customer": {"email": customer_email, "name": customer_name},
            },
        }
        return self._process_request(
            endpoint="/merchant/api/v1/transactions/disburse",
            method=HTTPMethod.POST,
            data=data,
        )

    def payout_to_mobile_money(
        self,
        reference: str,
        amount: int,
        currency: Currency,
        mobile_money_operator: str,
        mobile_number: str,
        customer_email: str,
        customer_name: str | None = None,
        narration: str | None = None,
    ) -> Response:
        data = {
            "reference": reference,
            "destination": {
                "type": "mobile_money",
                "amount": amount,
                "currency": currency.value,
                "narration": narration,
                "mobile_money": {
                    "operator": mobile_money_operator,
                    "mobile_number": mobile_number,
                },
                "customer": {"email": customer_email, "name": customer_name},
            },
        }
        return self._process_request(
            endpoint="/merchant/api/v1/transactions/disburse",
            method=HTTPMethod.POST,
            data=data,
        )

    def bulk_payout_to_bank_account(
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
            "payouts": [asdict(payout) for payout in payouts],
        }
        return self._process_request(
            endpoint="/api/v1/transactions/disburse/bulk",
            method=HTTPMethod.POST,
            data=data,
        )

    def get_payouts(self, bulk_reference: str) -> Response:
        return self._process_request(
            endpoint=f"/api/v1/transactions/bulk/{bulk_reference}/payout",
            method=HTTPMethod.GET,
        )

    def get_bulk_transaction(self, bulk_reference: str) -> Response:
        return self._process_request(
            endpoint=f"/api/v1/transactions/bulk/{bulk_reference}",
            method=HTTPMethod.GET,
        )

    def verify_payout_transaction(self, transaction_reference: str) -> Response:
        return self._process_request(
            endpoint=f"/merchant/api/v1/transactions/{transaction_reference}",
            method=HTTPMethod.GET,
        )
