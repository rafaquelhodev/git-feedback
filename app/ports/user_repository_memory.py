from typing import List
from app.adapters.user_repository import UserRepository
from app.domain.model import User


class UserRepositoryMemory(UserRepository):
    def __init__(self) -> None:
        self.__users: List[User] = list()

    def get(self, user_id: int) -> User:
        user = next((u for u in self.__users if u.id == user_id), None)
        return user

    def get_by_name(self, username: str) -> User:
        user = next((u for u in self.__users if u.name == username), None)
        return user

    def get_by_email(self, email: str) -> User:
        user = next((u for u in self.__users if u.email == email), None)
        return user

    def add(self, user: User) -> int:
        self.__users.append(user)
        return user.id
