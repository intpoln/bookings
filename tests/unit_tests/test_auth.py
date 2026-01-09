import pytest

from src.services.auth import AuthService


class TestAuthService:
    """Unit-тесты для AuthService"""

    def test_create_access_token(self):
        data = {"user_id": 1}
        token = AuthService().create_access_token(data)

        assert token
        assert isinstance(token, str)

    def test_create_refresh_token(self):
        data = {"user_id": 1}
        token = AuthService().create_refresh_token(data)

        assert token
        assert isinstance(token, str)

    def test_decode_access_token(self):
        data = {"user_id": 42}
        token = AuthService().create_access_token(data)

        payload = AuthService().decode_token(token)

        assert payload
        assert payload["user_id"] == data["user_id"]
        assert payload["type"] == "access"
        assert "exp" in payload

    def test_decode_refresh_token(self):
        data = {"user_id": 42}
        token = AuthService().create_refresh_token(data)

        payload = AuthService().decode_token(token)

        assert payload
        assert payload["user_id"] == data["user_id"]
        assert payload["type"] == "refresh"
        assert "exp" in payload

    def test_access_and_refresh_tokens_are_different(self):
        data = {"user_id": 1}
        access_token = AuthService().create_access_token(data)
        refresh_token = AuthService().create_refresh_token(data)

        # Токены должны быть разными (разный type и exp)
        assert access_token != refresh_token

    def test_hash_password(self):
        password = "MySecretPassword123"
        hashed = AuthService().hash_password(password)

        assert hashed
        assert hashed != password
        assert isinstance(hashed, str)

    def test_verify_password_correct(self):
        password = "MySecretPassword123"
        hashed = AuthService().hash_password(password)

        assert AuthService().verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        password = "MySecretPassword123"
        wrong_password = "WrongPassword"
        hashed = AuthService().hash_password(password)

        assert AuthService().verify_password(wrong_password, hashed) is False

    def test_hash_password_different_for_same_input(self):
        """bcrypt должен генерировать разные хеши для одного пароля (разная соль)"""
        password = "MySecretPassword123"
        hash1 = AuthService().hash_password(password)
        hash2 = AuthService().hash_password(password)

        assert hash1 != hash2
        # Но оба должны верифицироваться
        assert AuthService().verify_password(password, hash1) is True
        assert AuthService().verify_password(password, hash2) is True
