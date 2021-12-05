from datetime import timedelta
from app.domain.exceptions import UnauthorizedUser
from app.ports.jwt_auth import JwtAuth
from app.ports.password_hasher import PasswordHasher
from app.ports.user_repository import UserRepository


class LoginUser:
    def __init__(
        self,
        jwt_auth: JwtAuth,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        username: str,
        password: str,
        expire_minutes: int,
    ) -> None:
        self.jwt_auth = jwt_auth
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.username = username
        self.password = password
        self.expire_minutes = expire_minutes

    def execute(self):
        match_password, user = self.__authenticate_user()
        if not match_password or not user:
            raise UnauthorizedUser("Incorrect username or password")

        access_token_expires = timedelta(minutes=self.expire_minutes)
        access_token = self.jwt_auth.create_access_token(
            data={"sub": user.name}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def __authenticate_user(self):
        user = self.user_repository.get_by_name(self.username)
        if not user:
            return False, None

        match_password = self.password_hasher.is_hash_equal_to(
            self.password, user.password
        )

        return match_password, user
