import os
from typing import Type
from unittest import TestCase
from uuid import uuid4

from korapay_client import KorapayClient, Card, Currency, Response
from korapay_client.base_clients import AbstractBaseClient
from tests.test_clients.base_client_testcase import AbstractBaseClientTestCase
from httpx import codes


class SyncClientTestCase(AbstractBaseClientTestCase, TestCase):
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
        self.client: KorapayClient
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
