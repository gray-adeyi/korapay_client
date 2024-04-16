# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]



## [0.1.0] - 2024-04-16

### Added

- `KorapayClient` and `AsyncKorapayClient`
- `pydantic` for method and request payload models and validation
- package enums
    - `MobileMoneyOperator`
    - `Currency`
    - `PaymentChannel`
    - `Country`
- package models
    - `Responsse`
    - `AVS`
    - `Authorization`
    - `BankAccount`
    - `Customer`
    - `PayoutOrder`
    - `Card`
- package errors and exceptions
    - `MissingAPIKeyError`
    - `UnsupportedHTTPMethodError`
    - `ClientError`

[unreleased]: https://github.com/gray-adeyi/korapay_client/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/gray-adeyi/korapay_client/releases/tag/v0.1.0