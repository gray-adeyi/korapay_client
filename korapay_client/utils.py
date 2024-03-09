import json

from Crypto.Cipher import AES
from Crypto import Random
from binascii import hexlify

IV_LENGTH = 16
MAX_METADATA_FIELDS = 5
MAX_METADATA_FIELD_KEY_CHAR = 20


def encrypt_aes256(encryption_key: str, data: dict) -> str:
    if not encryption_key:
        raise ValueError(
            "An encryption key is required. please provide the encryption key in your account"
        )
    try:
        iv = Random.get_random_bytes(IV_LENGTH)
        encrypter = AES.new(encryption_key.encode("utf8"), AES.MODE_GCM, iv)
        data = json.dumps(data)
        cipher_text, auth_tag = encrypter.encrypt_and_digest(data.encode("utf8"))
        iv_as_hex = hexlify(iv).decode()
        cipher_text_as_hex = hexlify(cipher_text).decode()
        auth_tag_as_hex = hexlify(auth_tag).decode()
        encryption = iv_as_hex + ":" + cipher_text_as_hex + ":" + auth_tag_as_hex
        return encryption
    except ValueError as error:
        raise ValueError(
            f"Invalid encryption key. please provide the encryption key in your account. {error}"
        )


def validate_metadata(value: dict):
    if len(value.values()) > MAX_METADATA_FIELDS:
        raise ValueError("A maximum of 5 key/values is allowed")
    for key in value.keys():
        if len(key) > MAX_METADATA_FIELD_KEY_CHAR:
            raise ValueError(
                "A metadata field key should not contain characters"
                f" greater than {MAX_METADATA_FIELD_KEY_CHAR}"
            )
