import pytest
from app.adapters.jose_jwt_auth import JoseJwtAuth
from app.domain.exceptions import InvalidUserRegistration, UnauthorizedUser
from app.domain.model import User
from app.domain_usecases.login_user import LoginUser
from app.domain_usecases.register_user import RegisterUser
from app.adapters.password_hasher_passlib import PasswordPassLib
from app.adapters.user_repository_memory import UserRepositoryMemory


class TestRegisterUser:
    def test_register_user(self):
        user_repo = UserRepositoryMemory()
        password_lib = PasswordPassLib()

        register_user = RegisterUser(
            user_repository=user_repo,
            password_lib=password_lib,
            username="John",
            email="john@test.com",
            password="123456",
        )

        register_user.execute()

        user = user_repo.get_by_name("John")

        assert user.name == "John"
        assert user.email == "john@test.com"
        assert user.password != "123456"

    def test_error_when_username_is_used(self):
        user_repo = UserRepositoryMemory()

        user_john = User(name="John", email="john@test.com", password="123")
        user_repo.add(user_john)

        password_lib = PasswordPassLib()

        register_user = RegisterUser(
            user_repository=user_repo,
            password_lib=password_lib,
            username="John",
            email="john_2@test.com",
            password="123",
        )

        with pytest.raises(InvalidUserRegistration) as error:
            register_user.execute()
            assert "User name or email already in use" in str(error.value)

    def test_error_when_email_is_used(self):
        user_repo = UserRepositoryMemory()

        user_john = User(name="Mary", email="mary@test.com", password="123")
        user_repo.add(user_john)

        password_lib = PasswordPassLib()

        register_user = RegisterUser(
            user_repository=user_repo,
            password_lib=password_lib,
            username="mary-jane",
            email="mary@test.com",
            password="123",
        )

        with pytest.raises(InvalidUserRegistration) as error:
            register_user.execute()
            assert "User name or email already in use" in str(error.value)


class TestLoginUser:
    def test_login_user(self):
        user_repo = UserRepositoryMemory()

        register_user = RegisterUser(
            user_repository=user_repo,
            password_lib=PasswordPassLib,
            username="John",
            email="john@test.com",
            password="123456",
        )

        register_user.execute()

        login_user = LoginUser(
            jwt_auth=JoseJwtAuth,
            user_repository=user_repo,
            password_hasher=PasswordPassLib,
            username="John",
            password="123456",
            expire_minutes=30,
        )

        resp = login_user.execute()

        assert resp.get("access_token") != ""
        assert resp.get("access_token") != None
        assert resp.get("token_type") == "bearer"

    def test_login_user_with_incorrect_password(self):
        user_repo = UserRepositoryMemory()

        register_user = RegisterUser(
            user_repository=user_repo,
            password_lib=PasswordPassLib,
            username="John",
            email="john@test.com",
            password="123456",
        )

        register_user.execute()

        login_user = LoginUser(
            jwt_auth=JoseJwtAuth,
            user_repository=user_repo,
            password_hasher=PasswordPassLib,
            username="John",
            password="12345",
            expire_minutes=30,
        )

        with pytest.raises(UnauthorizedUser) as error:
            login_user.execute()
            assert "Incorrect username or password" in str(error.value)

    def test_login_user_that_doesnt_exist(self):
        user_repo = UserRepositoryMemory()

        register_user = RegisterUser(
            user_repository=user_repo,
            password_lib=PasswordPassLib,
            username="John",
            email="john@test.com",
            password="123456",
        )

        register_user.execute()

        login_user = LoginUser(
            jwt_auth=JoseJwtAuth,
            user_repository=user_repo,
            password_hasher=PasswordPassLib,
            username="Mary",
            password="123456",
            expire_minutes=30,
        )

        with pytest.raises(UnauthorizedUser) as error:
            login_user.execute()
            assert "Incorrect username or password" in str(error.value)
