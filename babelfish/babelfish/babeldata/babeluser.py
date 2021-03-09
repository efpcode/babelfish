from secrets import token_bytes
from hashlib import blake2b
from argon2 import PasswordHasher, exceptions
from typing import Union, Tuple
from ..babeldata.babeldb import BabelDB


class UserData:
    COUNTER: int = 3

    def __init__(
            self, username: str = None, password: str = None,
            email: str = None
    ):
        self.username = username
        self.password = password
        self.email = email

        if not self.password:
            self.password = b"password1"

    def __str__(self):
        return f"(username:{self.username} | password" \
               f":{'#'* len(self.password)} | email:{self.email})"

    def __repr__(self):
        return "UserData(b'demo_user', b'password1', " \
               "b'topiw96361@macosnine.com')"

    def hash_password(
            self, password: Union[str, bytes], salt: bytes = None) -> Tuple[
            bytes, str]:
        hasher = PasswordHasher()
        b_salt, hashed_password = self._pre_hash(password, b_salt=salt)
        hash = hasher.hash(hashed_password)
        return b_salt, hash

    def validate_user(
            self, password: Union[bytes, str], salt: bytes, dev_key: str):
        hasher = PasswordHasher()
        b_salt, password_hashed = self._pre_hash(password, b_salt=salt)

        try:
            hasher.verify(dev_key, password_hashed)

        except exceptions.HashingError as error:
            return f"Password is incorrect {error}"

        if hasher.check_needs_rehash(dev_key):
            return b_salt, hasher.hash(password_hashed)

        return b_salt, dev_key

    def _pre_hash(
            self, password: Union[str, bytes], b_salt: bytes = None) -> \
            Tuple[bytes, bytes]:
        if not b_salt:
            b_salt = UserData._salt_miner()

        hasher = blake2b(salt=b_salt)

        while True:

            try:
                hasher.update(password)

            except TypeError as error:
                print(f"{error}, will try to convert string to bytes")
                password = str.encode(password)
                continue

            else:
                return b_salt, hasher.digest()

# Static Methods
    @staticmethod
    def _salt_miner():
        """Methods returns 16 byte randomized token"""
        n = 16
        return token_bytes(nbytes=n)

    def _add_to_db(self):
        pass

    def _get_user_data(self):
        pass
