from abc import ABC, abstractmethod
from datetime import timedelta


class JwtAuth(ABC):
    @staticmethod
    @abstractmethod
    def create_access_token(
        data: dict, expires_delta: timedelta = timedelta(minutes=15)
    ) -> str:
        pass

    @staticmethod
    @abstractmethod
    def decode_access_token(token: str, validator_key: str) -> str:
        pass
