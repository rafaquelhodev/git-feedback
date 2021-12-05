from abc import ABC, abstractmethod

from app.domain.model import User


class UserRepository(ABC):
    @abstractmethod
    def get(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_by_name(self, username: str) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def add(self, user: User) -> int:
        pass
