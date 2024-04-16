## Charging a customer via debit card

```python
from uuid import uuid4
from korapay_client import Card, KorapayClient, Currency

card = Card(
    cvv="123", expiry_year="30", expiry_month="09", number="4084127883172787"
)
client = KorapayClient() # assumes you have set your credentials in your environmental variables
response = client.charge_via_card(
    reference=str(uuid4()),
    customer_name="John Doe",
    customer_email="johndoe@example.com",
    card=card,
    amount=1000,
    currency=Currency.NGN,
    redirect_url="https://github.com/gray-adeyi/korapay_client",
    metadata={"client_id": "qwerty"},
)
print(response)
```

## Authorizing a charge on a customer's card via pin

```python
from korapay_client import KorapayClient, Authorization

client = KorapayClient()  # assumes you have set your credentials in your environmental variables
response = client.authorize_card_charge(
    transaction_reference="KPY-CA-7VbzDPezNP7O9I7",
    authorization=Authorization.model_validate({"pin": "1234"}),
)
print(response)
```

## Charge a customer via mobile money

```python
from uuid import uuid4

from korapay_client import KorapayClient, Currency

client = KorapayClient()  # assumes you have set your credentials in your environmental variables
response = client.charge_via_mobile_money(
    reference=str(uuid4()),
    customer_email="johndoe@example.com",
    amount=1000,
    mobile_money_number="254711111111",
    currency=Currency.KES,
)
print(response)
```

## Bulk payouts to bank accounts

```python
from uuid import uuid4

from korapay_client import KorapayClient, Currency, PayoutOrder

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

client = KorapayClient()  # assumes you have set your credentials in your environmental variables
response = client.bulk_payout_to_bank_account(
    batch_reference=str(uuid4()),
    description="Test bulk payout",
    merchant_bears_cost=False,
    currency=Currency.NGN,
    payouts=[PayoutOrder.model_validate(data) for data in payout_orders],
)
print(response)
```