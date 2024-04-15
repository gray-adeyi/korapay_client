from decimal import Decimal

from pydantic import EmailStr, HttpUrl

from korapay_client.base_clients import AsyncBaseClient
from korapay_client.clients.client_method_parameter_validator import get_validator_class
from korapay_client.enums import (
    ClientMethod,
    HTTPMethod,
    Currency,
    PaymentChannel,
    Country,
    MobileMoneyOperator,
)
from korapay_client.models import (
    Card,
    Response,
    Authorization,
    PayoutOrder,
)
from korapay_client.utils import encrypt_aes256


class AsyncKorapayClient(AsyncBaseClient):
    """Asynchronous client for interfacing with Korapay"""

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
        """Accept debit card payments.

        Args:
            reference: A unique reference for the payment. The reference must be at least 8 characters long.
            customer_name: The name of your customer.
            customer_email: The email of your customer.
            card: A pydantic model representing your customer's card information. it can be imported directly from
                `korapay_client`.
            amount: The amount for the charge.
            currency: An enum representing the currency for the charge. E.g., `Currency.NGN`
            redirect_url: A URL to which we can redirect your customer after their payment is complete.
            metadata: A dictionary with a maximum of 5 fields/keys for storing additional information.
                Empty dictionaries are not allowed. Each field name (i.e., dictionary keys) can have a
                maximum length of 20 characters. Allowed characters: A-Z, a-z, 0-9, and -.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
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
        """Authorize a pending charge on a debit card.

        Args:
            transaction_reference: The reference to the pending charge returned as a response
                by korapay when the charge was initiated.
            authorization: A pydantic model with additional fields for authorizing the charge.
                The required field may vary depending on the type of authorization required.
                E.g., if a pending charge requires a pin for authorization
                `Authorization(pin='<customer-pin>')` is sufficient. Please refer to Korapay's
                Official documentation. The `Authorization` model can be imported directly from
                `korapay_client`

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
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
        """Resend one time password/pin for pending transaction.

        Args:
            transaction_reference: The reference to the pending charge returned as a response
                by korapay when the charge was initiated.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
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
        """Accept payments via bank transfers.

        Args:
            reference: A unique reference for the payment. The reference must be at least 8 characters long.
            customer_email: The email of your customer.
            amount: The amount for the charge.
            currency: An enum representing the currency for the charge. E.g., `Currency.NGN`. Currently, the
                only supported currency is `Currency.NGN`
            customer_name: The name of your customer.
            account_name: The account name that should be displayed when the account number is resolved.
            narration: Information/narration about the transaction.
            notification_url: A URL to which we can send the webhook notification for the transaction.
            merchant_bears_cost: This sets who bear the fees of the transaction. If it is set to `True`,
                the merchant will bear the fee. If it is set to `False`, the customer will bear the fee.
                By default, it is `False`.
            metadata: A dictionary with a maximum of 5 fields/keys for storing additional information.
                Empty dictionaries are not allowed. Each field name (i.e., dictionary keys) can have a
                maximum length of 20 characters. Allowed characters: A-Z, a-z, 0-9, and -.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
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
        """Create a virtual bank account.

        Virtual Bank Accounts (or Virtual Accounts) are a special type of bank account that you can use
        to receive payments from your customers multiple times.

        Args:
            account_name: The name of the Virtual Bank account.
            account_reference: Your unique reference to identify a virtual bank account.
            bank_code: This is the bank code of the bank providing the virtual bank account. E.g., `035` is the
                code for Wema Bank. Use `000` to create a virtual bank account in the sandbox environment.
            customer_name: The customer's name.
            bvn: The Bank Verification Number (BVN) of the customer.
            customer_email: The customer's email address.
            nin: The National Identity Number (NIN) of your customer.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
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
        """Retrieve a virtual bank account.

        Args:
            account_reference: Your unique reference for the virtual bank account.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
        return await self._process_request(
            endpoint=f"/merchant/api/v1/virtual-bank-account/{account_reference}",
            method=HTTPMethod.GET,
        )

    async def get_virtual_bank_account_transactions(
        self, account_number: str
    ) -> Response:
        """Retrieve transactions associated with a virtual bank account.

        Args:
            account_number: The account number of the virtual account.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
        return await self._process_request(
            endpoint=f"/merchant/api/v1/virtual-bank-account/transactions?account_number={account_number}",
            method=HTTPMethod.GET,
        )

    async def credit_sandbox_virtual_bank_account(
        self, account_number: str, amount: int | float | Decimal, currency: Currency
    ) -> Response:
        """Create a virtual bank account for testing/development.

        Args:
            account_number: This is the account number of the Fixed Virtual Bank Account.
            amount: This is the amount you want to credit to the account. The minimum
                amount is NGN 100, and the maximum amount is NGN 10,000,000.
            currency: An enum representing the currency for the account. Only `Currency.NGN` is accepted
                for now.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
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
        """Accept payments via mobile money.

        Note:
            Korapay currently only supports payments in Kenyan Shillings and Ghanaian Cedis. For Kenya,
            they support the following wallets; Mpesa, Airtel, and Equitel. While in Ghana, they support
            MTN Momo and Airtel Tigo.

        Args:
            reference: A unique reference for the payment. The reference must be at least 8 characters long.
            customer_email: The email of your customer.
            amount: The amount for the charge.
            mobile_money_number: The mobile number of the customer to be charged e.g., 254700000000.
            currency: An enum representing the currency the payment should be made in e.g., `Currency.KES`.
            notification_url: The webhook URL to be called when the transaction is complete.
            customer_name: The name of your customer.
            redirect_url: A URL to which we can redirect your customer after their payment is complete.
            merchant_bears_cost: This sets who bear the fees of the transaction. If it is set to `True`,
                the merchant will bear the fee. If it is set to `False`, the customer will bear the fee.
                By default, it is `False`.
            description: Information/narration about the transaction.
            metadata: A dictionary with a maximum of 5 fields/keys for storing additional information.
                Empty dictionaries are not allowed. Each field name (i.e., dictionary keys) can have a
                maximum length of 20 characters. Allowed characters: A-Z, a-z, 0-9, and -.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
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
        """Authorize a payment via mobile money.

        After initiating a charge via mobile money, the next step is based on the auth model returned
        in the response to the charge initiation. There are two ways of authorizing a transaction
        `OTP` and `STK_PROMPT`.
        After making the request to charge the number, if the status of the transaction is processing and
        auth_model is OTP, this means an OTP has been sent to the wallet owner's phone. You would need to
        collect the OTP to authorize the transaction.
        Collect the OTP sent to the customer’s phone and call this method with the
        OTP and the transaction reference.
        If the OTP verification is successful, an STK prompt will be sent to the wallet owner's phone for
        him to enter his PIN.

        Args:
            reference: The reference to the transaction.
            token: the otp or token from the customer.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
        return await self._process_request(
            endpoint="/merchant/api/v1/charges/mobile-money/authorize",
            method=HTTPMethod.POST,
            data={
                "reference": reference,
                "token": token,
            },
        )

    async def resend_mobile_money_otp(self, transaction_reference: str) -> Response:
        """Resend one time password/pin for a pending mobile money transaction.

        This method allows you to resend OTP in a situation where the initial OTP received had expired
        or was not received at all.

        Args:
            transaction_reference: The reference of the pending transaction.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
        return await self._process_request(
            endpoint="/merchant/api/v1/charges/mobile-money/resend-otp",
            method=HTTPMethod.POST,
            data={"transaction_reference": transaction_reference},
        )

    async def resend_stk(self, transaction_reference: str) -> Response:
        """Resend STK prompt.

        This method allows you to resend the STK prompt in a situation where the initial STK prompt
         received had expired or was not received at all.

         Args:
            transaction_reference: The reference of the pending transaction.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
        return await self._process_request(
            endpoint="/merchant/api/v1/charges/mobile-money/resend-stk",
            method=HTTPMethod.POST,
            data={"transaction_reference": transaction_reference},
        )

    async def authorize_stk(self, reference: str, pin: str) -> Response:
        """Authorize STK prompts in test/development.

        This method allows you to authorize the transaction in the Sandbox environment. It is meant to
        simulate a wallet owner entering their wallet PIN at the STK prompt.

        Args:
            reference: The reference of the pending transaction.
            pin: The simulated customer's pin

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
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
        """Initiate a charge on your customer supporting multiple payment channels.

        This method allows you to configure payment channels of your choice when initiating a payment.

        Args:
            reference: Your transaction reference. Must be unique for every transaction.
            amount: The amount to charge the customer.
            currency: An enum representing the currency to charge the customer in. E.g., `Currency.GHS`.
            narration: The description of the transaction.
            notification_url: The webhook URL to be called when the transaction is complete.
            customer_email: The customer's email.
            customer_name: The customer's name.
            channels: A list of `PaymentChannel` enum representing the payment channels you want to support
                for accepting the payments. E.g., `[PaymentChannel.CARD, PaymentChannel.BANK_TRANSFER]`
            default_channel: A enum representing the preferred payment channel when multiple payment channels
                are supported. E.g., `PaymentChannel.MOBILE_MONEY`
            redirect_url: The URL to redirect your customer when the transaction is complete.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
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
        """Retrieve a charge.

        Args:
            reference: The reference of the charge.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
        return await self._process_request(
            endpoint=f"/merchant/api/v1/charges/{reference}", method=HTTPMethod.GET
        )

    async def resolve_bank_account(
        self, bank_code: str, account_number: str
    ) -> Response:
        """Resolves a bank account.

        This method can be used to validate if an account number is valid for the specified bank.

        Args:
            bank_code: The code for the bank the account number belongs to.
            account_number: The account number to be resolved.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
        return await self._process_request(
            endpoint="/merchant/api/v1/misc/banks/resolve",
            method=HTTPMethod.POST,
            data={"bank": bank_code, "account": account_number},
        )

    async def get_balances(self) -> Response:
        """Retrieve all your pending and available balances.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
        return await self._process_request(
            endpoint="/merchant/api/v1/balances",
            method=HTTPMethod.GET,
        )

    async def get_banks(self, country: Country) -> Response:
        """Retrieve a list of all banks supported by Korapay and their properties.

        Args:
            country: An enum representing the country to retrieve the banks from. E.g., `Country.NIGERIA`.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
        return await self._process_request(
            endpoint=f"/merchant/api/v1/misc/banks?countryCode={country.value}",
            method=HTTPMethod.GET,
            use_public_auth=True,
        )

    async def get_mmo(self, country: Country) -> Response:
        """Retrieve a list of all mobile money operators supported by Korapay and their properties.

        Args:
            country: An enum representing the country to retrieve the MMOs from. E.g., `Country.GHANA`.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
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
        """Initiate a single disbursement to a bank account.

        Args:
            reference: Unique transaction reference.
            amount: The transaction amount.
            currency: A enum representing the currency to disburse in. E.g., `Currency.NGN`
            bank_code: The Recipient bank code. Bank_codes on testmode with Test keys to simulate
                a successful transaction are 044, 033, 058 i.e., Access, UBA and GTB respectively,
                other banks would simulate a failed transaction on testmode with testkeys.
            account_number: The recipient's account number.
            customer_email: The customer's email.
            narration: The transaction's narration or description.
            customer_name: The customer's name.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
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
        """Initiate a single disbursement to a mobile money account.

        Args:
            reference: Unique transaction reference.
            amount: The transaction amount.
            currency: A enum representing the currency to disburse in. E.g., `Currency.NGN`
            mobile_money_operator: An enum or str representing the mobile money operator. E.g.,
                `MobileMoneyOperator.AIRTEL_KENYA`.
            mobile_number: The recipient's mobile money number.
            customer_email: The customer's email.
            customer_name: The customer's name.
            narration: The transaction's narration or description.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
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
        """Initiate a bulk payout to bank accounts.

        Args:
            batch_reference: A reference used to identify the batch.
            description: A narration for the batch.
            merchant_bears_cost: This sets who bear the fees of the transaction. If it is set to `True`,
                the merchant will bear the fee. If it is set to `False`, the customer will bear the fee.
                By default, it is `False`.
            currency: A enum representing the currency to disburse in. E.g., `Currency.NGN`
            payouts: A list of `PayoutOrder` which is a pydantic model representing individual recipient
                information in the bulk payout. This model can be imported directly from `korapay_client`

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
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
        """Retrieve a bulk payout.

        Args:
            bulk_reference: The reference of the bulk payout to retrieve.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
        return await self._process_request(
            endpoint=f"/api/v1/transactions/bulk/{bulk_reference}/payout",
            method=HTTPMethod.GET,
        )

    async def get_bulk_transaction(self, bulk_reference: str) -> Response:
        """Retrieve the transactions in a bulk payout

        Args:
            bulk_reference: The reference of the bulk payout whose transactions you to retrieve.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
        return await self._process_request(
            endpoint=f"/api/v1/transactions/bulk/{bulk_reference}",
            method=HTTPMethod.GET,
        )

    async def get_payout_transaction(self, transaction_reference: str) -> Response:
        """Retrieve the status and details of a disbursement through the reference.

        This method can be used to verify the status of a payout transaction.

        Args:
            transaction_reference: The reference of the payout.

        Returns:
            A pydantic model containing the result of the request.

        Raises:
            ClientError: When an error or exception occurs while making the request to Korapay.
        """
        return await self._process_request(
            endpoint=f"/merchant/api/v1/transactions/{transaction_reference}",
            method=HTTPMethod.GET,
        )
