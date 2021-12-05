from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.domain.exceptions import InvalidCredentials

from app.ports.jwt_auth import JwtAuth

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


class JoseJwtAuth(JwtAuth):
    @staticmethod
    def create_access_token(
        data: dict, expires_delta: timedelta = timedelta(minutes=15)
    ) -> str:
        to_encode = data.copy()

        expire = datetime.utcnow() + expires_delta

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str, validator_key: str) -> str:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get(validator_key)
            return username
        except JWTError:
            raise InvalidCredentials("Invalid credentials")
