import pytest
from app.domain.exceptions import InvalidUserRegistration
from app.domain.model import User
from app.domain_usecases.register_user import RegisterUser
from app.adapters.password_passlib import PasswordPassLib
from app.ports.user_repository_memory import UserRepositoryMemory


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
