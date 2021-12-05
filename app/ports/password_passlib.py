from passlib.hash import pbkdf2_sha256

from app.adapters.password import Password


class PasswordPassLib(Password):
    @staticmethod
    def hash(plain_password: str) -> str:
        hash = pbkdf2_sha256.hash(plain_password)
        return hash

    @staticmethod
    def is_hash_equal_to(plain_password: str, hash: str) -> bool:
        return pbkdf2_sha256.verify(plain_password, hash)
