import random

from dotenv import load_dotenv
from abc import ABC, abstractmethod
from typing import Type

from korapay_client.base_clients import AbstractBaseClient


class AbstractClientTestCase(ABC):
    @classmethod
    def setUpClass(cls):
        client_class = cls.get_client_class()
        cls.public_key = "test-public-key"
        cls.secret_key = "test-secret-key"
        cls.encryption_key = "test-encryption-key"
        cls.client_with_credentials_from_instantiation = client_class(
            public_key=cls.public_key,
            secret_key=cls.secret_key,
            encryption_key=cls.encryption_key,
        )
        load_dotenv()
        # credentials are loaded from environmental variables
        cls.client = client_class()

    @classmethod
    @abstractmethod
    def get_client_class(cls) -> Type[AbstractBaseClient]: ...

    def _generate_number(self, length: int) -> int:
        return random.randint(10 ** (length - 1), 10**length - 1)

    def _generate_bvn(self) -> str:
        return str(self._generate_number(11))
