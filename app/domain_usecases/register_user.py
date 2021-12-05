from app.ports.password import Password
from app.adapters.user_repository import UserRepository
from app.domain.exceptions import InvalidUserRegistration
from app.domain.model import User


class RegisterUser:
    def __init__(
        self,
        user_repository: UserRepository,
        password_lib: Password,
        username: str,
        email: str,
        password: str,
    ) -> None:
        self.user_repository = user_repository
        self.password_lib = password_lib
        self.username = username
        self.email = email
        self.password = password

    def execute(self) -> int:
        is_username_used = self.user_repository.get_by_name(self.username)
        if is_username_used:
            raise InvalidUserRegistration("User name or email already in use")

        is_email_used = self.user_repository.get_by_email(self.email)
        if is_email_used:
            raise InvalidUserRegistration("User name or email already in use")

        hashed_password = self.password_lib.hash(self.password)

        user = User(name=self.username, email=self.email, password=hashed_password)

        user_id = self.user_repository.add(user)
        return user_id
