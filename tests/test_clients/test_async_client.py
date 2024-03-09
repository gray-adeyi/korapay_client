from typing import Type
from unittest import IsolatedAsyncioTestCase

from korapay_client import AsyncKorapayClient
from korapay_client.base_clients import AbstractBaseClient
from tests.test_clients.base_client_testcase import AbstractBaseClientTestCase


class AsyncClientTestCase(AbstractBaseClientTestCase, IsolatedAsyncioTestCase):
    @classmethod
    def get_client_class(cls) -> Type[AbstractBaseClient]:
        return AsyncKorapayClient
