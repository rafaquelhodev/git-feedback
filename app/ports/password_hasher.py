from abc import abstractmethod


class PasswordHasher:
    @staticmethod
    @abstractmethod
    def hash(plain_password: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def is_hash_equal_to(plain_password: str, hash: str) -> bool:
        pass
