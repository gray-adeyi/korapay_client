import os
from typing import Type
from unittest import TestCase
from uuid import uuid4

from korapay_client import (
    KorapayClient,
    Currency,
    Response,
    Country,
    Authorization,
    PayoutOrder,
    ClientError,
    Card,
    MobileMoneyOperator,
)
from korapay_client.base_clients import AbstractBaseClient
from tests.test_clients.base_client_testcase import AbstractClientTestCase
from httpx import codes


class SyncClientTestCase(AbstractClientTestCase, TestCase):
    client: KorapayClient

    @classmethod
    def get_client_class(cls) -> Type[AbstractBaseClient]:
        return KorapayClient

    def test_when_client_credentials_is_passed_on_instantiation_overrides_values_set_in_env(
        self,
    ):
        public_key_in_env = os.environ[self.client.KORAPAY_ENV_PUBLIC_KEY_NAME]
        secret_key_in_env = os.environ[self.client.KORAPAY_ENV_SECRET_KEY_NAME]
        encryption_key_in_env = os.environ[self.client.KORAPAY_ENV_ENCRYPTION_KEY_NAME]

        self.assertNotEqual(
            self.client_with_credentials_from_instantiation._public_key,
            public_key_in_env,
        )
        self.assertNotEqual(
            self.client_with_credentials_from_instantiation._secret_key,
            secret_key_in_env,
        )
        self.assertNotEqual(
            self.client_with_credentials_from_instantiation._encryption_key,
            encryption_key_in_env,
        )

        self.assertEqual(
            self.client_with_credentials_from_instantiation._public_key, self.public_key
        )
        self.assertEqual(
            self.client_with_credentials_from_instantiation._secret_key, self.secret_key
        )
        self.assertEqual(
            self.client_with_credentials_from_instantiation._encryption_key,
            self.encryption_key,
        )

    def test_client_can_charge_via_card(self):
        card = Card(
            cvv="123", expiry_year="30", expiry_month="09", number="4084127883172787"
        )
        response = self.client.charge_via_card(
            reference=str(uuid4()),
            customer_name="John Doe",
            customer_email="johndoe@example.com",
            card=card,
            amount=1000,
            currency=Currency.NGN,
            redirect_url="https://github.com/gray-adeyi/korapay_client",
            metadata={"client_id": "qwerty"},
        )
        self.assertIsInstance(response, Response)
        self.assertTrue(codes.is_success(response.status_code))
        self.assertTrue(response.status)
        self.assertEqual(response.message, "Card charged successfully")

    def test_client_can_authorize_card_charge(self):
        # TODO: change form using an already processed transaction
        response = self.client.authorize_card_charge(
            transaction_reference="KPY-CA-7VbzDPezNP7O9I7",
            authorization=Authorization.model_validate({"pin": "1234"}),
        )
        self.assertEqual(response.status_code, codes.CONFLICT)

    def test_client_can_resend_card_otp(self):
        # TODO: change form using an already processed transaction
        response = self.client.resend_card_otp(
            transaction_reference="KPY-CA-7VbzDPezNP7O9I7",
        )
        self.assertEqual(response.status_code, codes.CONFLICT)

    def test_client_can_charge_via_bank_transfer(self):
        response = self.client.charge_via_bank_transfer(
            reference=str(uuid4()),
            customer_email="johndoe@example.com",
            amount=1000,
            currency=Currency.NGN,
            metadata={"name": "john doe"},
        )
        self.assertTrue(codes.is_success(response.status_code))
        self.assertTrue(response.status)

    def test_client_can_create_virtual_bank_account(self):
        response = self.client.create_virtual_bank_account(
            account_name="John Doe Virtual Account",
            account_reference=str(uuid4()),
            bank_code="000",
            customer_name="John Doe",
            bvn=self._generate_bvn(),
        )
        self.assertTrue(codes.is_success(response.status_code))
        self.assertTrue(response.status)

    def test_client_can_get_virtual_bank_account(self):
        response = self.client.get_virtual_bank_account(
            account_reference="716b4728-7fca-43e8-916a-3a4c0f298165"
        )
        self.assertTrue(codes.is_success(response.status_code))
        self.assertTrue(response.status)

    def test_client_can_get_virtual_bank_account_transactions(self):
        response = self.client.get_virtual_bank_account_transactions(
            account_number="1110026499"
        )
        self.assertTrue(codes.is_success(response.status_code))
        self.assertTrue(response.status)

    def test_client_can_credit_sandbox_virtual_bank_account(self):
        response = self.client.credit_sandbox_virtual_bank_account(
            account_number="1110026499", amount=1000, currency=Currency.NGN
        )
        self.assertTrue(codes.is_success(response.status_code))
        self.assertTrue(response.status)

    def test_client_can_charge_via_mobile_money(self):
        response = self.client.charge_via_mobile_money(
            reference=str(uuid4()),
            customer_email="johndoe@example.com",
            amount=1000,
            mobile_money_number="254711111111",
            currency=Currency.KES,
        )
        self.assertTrue(codes.is_success(response.status_code))
        self.assertTrue(response.status)

    def test_client_can_authorize_mobile_money_charge(self):
        # TODO: replace use of already processed token
        response = self.client.authorize_mobile_money_charge(
            reference="KPY-CA-IeO1NKLtkB4k", token="123456"
        )
        self.assertEqual(response.status_code, codes.CONFLICT)

    def test_client_can_resend_mobile_money_otp(self):
        response = self.client.resend_mobile_money_otp(
            transaction_reference="KPY-CA-IeO1NKLtkB4k"
        )
        self.assertEqual(response.status_code, codes.CONFLICT)

    def test_client_can_resend_stk(self):
        response = self.client.resend_stk(transaction_reference="KPY-CA-IeO1NKLtkB4k")
        self.assertEqual(response.status_code, codes.CONFLICT)

    def test_client_can_authorize_stk(self):
        response = self.client.authorize_stk(
            reference="KPY-CA-IeO1NKLtkB4k", pin="1234"
        )
        self.assertEqual(response.status_code, codes.CONFLICT)

    def test_client_can_initiate_charge(self):
        response = self.client.initiate_charge(
            reference=str(uuid4()),
            amount=500.60,
            currency=Currency.NGN,
            narration="test charge",
            notification_url="https://example.com",
            customer_email="johndoe@example.com",
        )
        self.assertTrue(codes.is_success(response.status_code))
        self.assertTrue(response.status)

    def test_client_can_get_charge(self):
        response = self.client.get_charge(
            reference="3016305c-fb05-4ef3-ad3a-96bb4c80eb7f"
        )
        self.assertTrue(codes.is_success(response.status_code))
        self.assertTrue(response.status)

    def test_client_can_resolve_bank_account(self):
        response = self.client.resolve_bank_account(
            bank_code="033", account_number="0000000000"
        )
        self.assertTrue(codes.is_success(response.status_code))
        self.assertTrue(response.status)

    def test_client_can_get_balances(self):
        response = self.client.get_balances()
        self.assertTrue(codes.is_success(response.status_code))
        self.assertEqual(response.message, "success")

    def test_client_can_get_banks(self):
        response = self.client.get_banks(country=Country.NIGERIA)
        self.assertTrue(codes.is_success(response.status_code))
        self.assertEqual(response.message, "Successful")

    def test_client_can_get_mmo(self):
        response = self.client.get_mmo(country=Country.NIGERIA)
        self.assertTrue(codes.is_success(response.status_code))
        self.assertEqual(response.message, "Successful")

    def test_client_can_payout_to_bank_account(self):
        response = self.client.payout_to_bank_account(
            reference=str(uuid4()),
            amount=1000,
            currency=Currency.NGN,
            bank_code="033",
            account_number="0000000000",
            customer_email="johndoe@example.com",
        )
        self.assertTrue(codes.is_success(response.status_code))
        self.assertTrue(response.status)

    def test_client_can_payout_to_mobile_money(self):
        response = self.client.payout_to_mobile_money(
            reference=str(uuid4()),
            amount=1000,
            currency=Currency.KES,
            mobile_money_operator=MobileMoneyOperator.SAFARICOM_KENYA,
            mobile_number="254711111111",
            customer_email="johndoe@example.com",
        )
        self.assertTrue(codes.is_success(response.status_code))
        self.assertTrue(response.status)

    def test_client_can_bulk_payout_to_bank_account(self):
        payout_orders = [
            {
                "reference": str(uuid4()),
                "amount": 2500,
                "bank_account": {"bank_code": "033", "account_number": "0000000000"},
                "customer": {"email": "johndoe@example.com"},
            },
            {
                "reference": str(uuid4()),
                "amount": 2500,
                "bank_account": {"bank_code": "035", "account_number": "0000000000"},
                "customer": {"email": "johndoe@example.com"},
            },
        ]
        with self.assertRaises(ClientError) as error:
            self.client.bulk_payout_to_bank_account(
                batch_reference=str(uuid4()),
                description="Test bulk payout",
                merchant_bears_cost=False,
                currency=Currency.NGN,
                payouts=[PayoutOrder.model_validate(data) for data in payout_orders],
            )
        self.assertEqual(
            str(error.exception),
            (
                "Unable to parse server response as json"
                " data: status_code: 200 content: b'Welcome to Kora'"
            ),
        )

    def test_client_can_get_payouts(self):
        with self.assertRaises(ClientError) as error:
            self.client.get_payouts(
                bulk_reference="b4cb385b-6a8b-4d61-94da-e11619490195"
            )
        self.assertEqual(
            str(error.exception),
            (
                "Unable to parse server response as json"
                " data: status_code: 200 content: b'Welcome to Kora'"
            ),
        )

    def test_client_can_get_bulk_transaction(self):
        with self.assertRaises(ClientError) as error:
            self.client.get_bulk_transaction(
                bulk_reference="b4cb385b-6a8b-4d61-94da-e11619490195"
            )
        self.assertEqual(
            str(error.exception),
            (
                "Unable to parse server response as json"
                " data: status_code: 200 content: b'Welcome to Kora'"
            ),
        )

    def test_client_can_get_payout_transaction(self):
        response = self.client.get_payout_transaction(
            transaction_reference="70298986-4da3-4e73-b79a-9c9ba60bda98"
        )
        self.assertTrue(codes.is_success(response.status_code))
        self.assertTrue(response.status)
