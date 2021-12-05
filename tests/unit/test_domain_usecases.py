from app.domain_usecases.register_user import RegisterUser
from app.ports.password_passlib import PasswordPassLib
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
