import os
import sys
from abc import ABC, abstractmethod
from json import JSONDecodeError

import httpx

from korapay_client.enums import HTTPMethod
from korapay_client.exceptions import (
    MissingAPIKeyError,
    UnsupportedHTTPMethodError,
    ClientError,
)
from korapay_client._metadata import __version__
from korapay_client.models import Response


class AbstractBaseClient(ABC):
    KORAPAY_ENV_PUBLIC_KEY_NAME = "KORAPAY_PUBLIC_KEY"
    KORAPAY_ENV_SECRET_KEY_NAME = "KORAPAY_SECRET_KEY"
    KORAPAY_ENV_ENCRYPTION_KEY_NAME = "KORAPAY_ENCRYPTION_KEY"

    def __init__(
        self,
        public_key: str | None = None,
        secret_key: str | None = None,
        encryption_key: str | None = None,
    ):
        self._public_key = None
        self._secret_key = None
        self._encryption_key = None

        self._load_public_key(public_key)
        self._load_secret_key(secret_key)
        self._load_encryption_key(encryption_key)

    @property
    def _base_url(self) -> str:
        return "https://api.korapay.com"

    @property
    def _base_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "User-Agent": f"korapay-client-{__version__} Python-{sys.version}",
        }

    @property
    def _headers_with_public_authorization(self):
        headers = self._base_headers
        headers["Authorization"] = f"Bearer {self._public_key}"
        return headers

    @property
    def _headers_with_secret_authorization(self):
        headers = self._base_headers
        headers["Authorization"] = f"Bearer {self._secret_key}"
        return headers

    @abstractmethod
    def _process_request(
        self,
        endpoint: str,
        method: HTTPMethod,
        data: dict | list | None = None,
        use_public_auth: bool = False,
    ) -> Response: ...

    def _serialize_request_payload(
        self,
        endpoint: str,
        method: HTTPMethod,
        data: dict | list | None = None,
        use_public_auth: bool = False,
    ) -> dict:
        payload = {
            "url": f"{self._base_url}{endpoint}",
            "json": data,
            "headers": self._headers_with_secret_authorization
            if not use_public_auth
            else self._headers_with_public_authorization,
        }
        if method in {HTTPMethod.GET, HTTPMethod.DELETE}:
            payload.pop("json", None)
        return payload

    @staticmethod
    def _deserialize_response(raw_response: httpx.Response) -> Response:
        try:
            response_body = raw_response.json()
        except JSONDecodeError:
            raise ClientError(
                (
                    "Unable to parse server response as json data: status_code:"
                    f" {raw_response.status_code} content: {raw_response.content}"
                )
            )
        return Response(
            status_code=raw_response.status_code,
            status=response_body.get("status", False),
            message=response_body.get("message", ""),
            data=response_body.get("data", None),
        )

    def _load_public_key(self, public_key: str | None = None):
        if public_key:
            self._public_key = public_key
        else:
            self._public_key = os.getenv(self.KORAPAY_ENV_PUBLIC_KEY_NAME, None)
        if not self._public_key:
            raise MissingAPIKeyError(
                "Client could not find any public key. Please provide a public key on instantiation of this "
                f"client or provide it in your environmental variables as {self.KORAPAY_ENV_PUBLIC_KEY_NAME}"
            )

    def _load_secret_key(self, secret_key: str | None = None):
        if secret_key:
            self._secret_key = secret_key
        else:
            self._secret_key = os.getenv(self.KORAPAY_ENV_SECRET_KEY_NAME, None)
        if not self._secret_key:
            raise MissingAPIKeyError(
                "Client could not find any secret key. Please provide a secret key on instantiation of this "
                f"client or provide it in your environmental variables as {self.KORAPAY_ENV_SECRET_KEY_NAME}"
            )

    def _load_encryption_key(self, encryption_key: str | None = None):
        if encryption_key:
            self._encryption_key = encryption_key
        else:
            self._encryption_key = os.getenv(self.KORAPAY_ENV_ENCRYPTION_KEY_NAME, None)
        if not self._encryption_key:
            raise MissingAPIKeyError(
                "Client could not find any encryption key. Please provide an encryption key on instantiation of "
                f"this client or provide it in your environmental variables as {self.KORAPAY_ENV_ENCRYPTION_KEY_NAME}"
            )


class BaseClient(AbstractBaseClient):
    def _process_request(
        self,
        endpoint: str,
        method: HTTPMethod,
        data: dict | list | None = None,
        use_public_auth: bool = False,
    ) -> Response:
        request_handlers = {
            HTTPMethod.GET: httpx.get,
            HTTPMethod.POST: httpx.post,
            HTTPMethod.PUT: httpx.put,
            HTTPMethod.PATCH: httpx.patch,
            HTTPMethod.DELETE: httpx.delete,
            HTTPMethod.OPTIONS: httpx.options,
            HTTPMethod.HEAD: httpx.head,
        }
        handler = request_handlers.get(method)

        if not handler:
            raise UnsupportedHTTPMethodError(
                "HTTP Request method not recognized or supported"
            )
        payload = self._serialize_request_payload(
            endpoint=endpoint, method=method, data=data, use_public_auth=use_public_auth
        )
        try:
            raw_response = handler(**payload)
            return self._deserialize_response(raw_response)
        except httpx.RequestError as error:
            raise ClientError(
                f"An error occurred while making a request to Korapay servers. Error: {error}"
            )


class AsyncBaseClient(AbstractBaseClient):
    async def _process_request(
        self,
        endpoint: str,
        method: HTTPMethod,
        data: dict | list | None = None,
        use_public_auth: bool = False,
    ) -> Response:
        async with httpx.AsyncClient() as client:
            handler = getattr(client, method.value.lower(), None)

            if not handler:
                raise UnsupportedHTTPMethodError(
                    "HTTP Request method not recognized or supported"
                )
            payload = self._serialize_request_payload(
                endpoint=endpoint,
                method=method,
                data=data,
                use_public_auth=use_public_auth,
            )
            try:
                raw_response = await handler(**payload)
                return self._deserialize_response(raw_response)
            except httpx.RequestError as error:
                raise ClientError(
                    f"An error occurred while making a request to Korapay servers. Error: {error}"
                )
