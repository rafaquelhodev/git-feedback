from app.domain.exceptions import InvalidCredentials
from app.domain.model import User
from app.ports.jwt_auth import JwtAuth
from app.ports.user_repository import UserRepository


class AuthenticateUser:
    def __init__(
        self, jwt_auth: JwtAuth, user_repository: UserRepository, token: str
    ) -> None:
        self.jwt_auth = jwt_auth
        self.user_repository = user_repository
        self.token = token

    def execute(self) -> User:
        username = self.jwt_auth.decode_access_token(self.token, "sub")
        if username is None:
            raise InvalidCredentials("Invalid credentials")

        user = self.user_repository.get_by_name(username=username)
        if user is None:
            raise InvalidCredentials("Invalid credentials")
        return user
