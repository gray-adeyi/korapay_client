## Requirements

`korapay_client` requires `python >=3.10`

## Installation

```bash
pip install korapay-client
```

## Trying it out

- Install `korapay-client` into a virtual environment as described in the installation guide.
- Set your credentials i.e. `KORAPAY_PUBLIC_KEY`, `KORAPAY_SECRET_KEY` & `KORAPAY_ENCRYPTION_KEY`
    in your environmental variables.
- Start a python REPL in your virtual env by running `python`
- Follow the REPL dump below.

```bash
Python 3.10.13 (main, Feb 25 2024, 04:16:53) [Clang 17.0.6 ] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from korapay_client import KorapayClient
>>> client = KorapayClient() # assumes you have set your credentials in your environmental variables
>>> response = client.get_balances()
>>> print(response.status_code)
200
>>> print(response)
status_code=200 status=True message='success' data={'GHS': {'pending_balance': 0, 'available_balance': 5000000}, 'KES': {'pending_balance': 0, 'available_balance': 4992000}, 'NGN': {'pending_balance': 0, 'available_balance': 5024016.45}, 'USD': {'pending_balance': 0, 'available_balance': 5000000}}
>>> 
```

!!! info

    you can pass your credentials directly into `KorapayClient` for convenience while testing but it is discouraged.
    ```python
        from korapay_client import KorapayClient
        client = KorapayClient(public_key='<your-public-key>', secret_key='<your-secret-key>',
            encryption_key='<your-encryption-key>')
    ```

### Trying out the async client.

The previous section demonstrates how to use `KorapayClient` which is a synchronous client, 
`korapay_client` also provides `AsyncKorapayClient` an asynchronous equivalent of the 
`KorapayClient`. The method names for both clients are identical but the methods on the
`AsynchronousClient` are awaitable. Follow the steps below to try out the asynchronous
client.

- Install `korapay_client` into a virtual environment as described in the installation guide.
- Set your credentials i.e. `KORAPAY_PUBLIC_KEY`, `KORAPAY_SECRET_KEY` & `KORAPAY_ENCRYPTION_KEY`
    in your environmental variables.
- Start an asyncio python REPL in your virtual env by running `python -m asyncio`
- Follow the REPL dump below.

```bash
asyncio REPL 3.10.13 (main, Feb 25 2024, 04:16:53) [Clang 17.0.6 ] on linux
Use "await" directly instead of "asyncio.run()".
Type "help", "copyright", "credits" or "license" for more information.
>>> import asyncio
>>> from korapay_client import AsyncKorapayClient
>>> client = AsyncKorapayClient() # assumes you have set your credentials in your environmental variables
>>> response = await client.get_balances()
>>> print(response.status_code)
200
>>> print(response)
status_code=200 status=True message='success' data={'GHS': {'pending_balance': 0, 'available_balance': 5000000}, 'KES': {'pending_balance': 0, 'available_balance': 4992000}, 'NGN': {'pending_balance': 0, 'available_balance': 5024016.45}, 'USD': {'pending_balance': 0, 'available_balance': 5000000}}
>>> 
```

!!! warning

    you may get a `ClientError` raised when you run `response = client.get_balances()` in the synchronous context or
    `response = await client.get_balances()` in the asynchronous context. This could be as a result of a timeout or
    other network related issues. In your projects, you want to make sure you handle this error appropriately, all
    client methods that make network calls may raise `ClientError`. But for just trying it how here. running those
    lines again might be sufficient to resolve the issue and also ensure you have an adequate internet connection.