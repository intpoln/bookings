import pytest


class TestAuthRegister:
    """Тесты регистрации пользователей"""

    @pytest.mark.parametrize(
        "username, email, password, status_code",
        [
            ("User1", "user1@test.com", "Password123", 201),
            ("User2", "user2@test.com", "Password123", 201),
            ("User3", "user3@test.com", "Password123", 201),
            ("User3", "user3@test.com", "Password123", 409),  # Дубликат
        ],
    )
    async def test_register_user(self, username, email, password, status_code, ac):
        response = await ac.post(
            "/auth/register",
            json={"username": username, "email": email, "password": password},
        )
        assert response.status_code == status_code


class TestAuthLogin:
    """Тесты авторизации и работы с токенами"""

    @pytest.mark.parametrize(
        "email, password, status_code",
        [
            ("user1@test.com", "Password123", 201),
            ("user2@test.com", "Password123", 201),
            ("nonexistent@test.com", "Password123", 401),  # Несуществующий пользователь
            ("user1@test.com", "WrongPassword", 401),  # Неверный пароль
        ],
    )
    async def test_login_user(self, email, password, status_code, ac):
        response = await ac.post("/auth/login", json={"email": email, "password": password})
        assert response.status_code == status_code

        if status_code == 201:
            data = response.json()
            assert "access_token" in data
            assert "refresh_token" in data
            assert response.cookies.get("access_token")
            assert response.cookies.get("refresh_token")

    async def test_login_and_get_me(self, ac):
        # Login
        login_response = await ac.post(
            "/auth/login",
            json={"email": "user1@test.com", "password": "Password123"},
        )
        assert login_response.status_code == 201

        # Get current user info
        me_response = await ac.get("/auth/me", cookies=login_response.cookies)
        assert me_response.status_code == 200

        user_data = me_response.json()
        assert "id" in user_data
        assert user_data["email"] == "user1@test.com"
        assert "password" not in user_data
        assert "hashed_password" not in user_data

    async def test_logout(self, ac):
        # Login first
        login_response = await ac.post(
            "/auth/login",
            json={"email": "user1@test.com", "password": "Password123"},
        )
        assert login_response.status_code == 201

        # Logout
        logout_response = await ac.post("/auth/logout", cookies=login_response.cookies)
        assert logout_response.status_code == 200
        assert "access_token" not in logout_response.cookies
        assert "refresh_token" not in logout_response.cookies


class TestAuthRefresh:
    """Тесты обновления токенов"""

    async def test_refresh_tokens(self, ac):
        # Login to get tokens
        login_response = await ac.post(
            "/auth/login",
            json={"email": "user1@test.com", "password": "Password123"},
        )
        assert login_response.status_code == 201
        old_access_token = login_response.json()["access_token"]

        # Refresh tokens
        refresh_response = await ac.post("/auth/refresh", cookies=login_response.cookies)
        assert refresh_response.status_code == 200

        data = refresh_response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        # New access token should be different (different exp time)
        assert data["access_token"] != old_access_token

    async def test_refresh_without_token(self, ac):
        response = await ac.post("/auth/refresh")
        assert response.status_code == 401
        assert "Refresh token отсутствует" in response.json()["detail"]

    async def test_refresh_with_invalid_token(self, ac):
        response = await ac.post("/auth/refresh", cookies={"refresh_token": "invalid_token"})
        assert response.status_code == 401

    async def test_me_without_token(self, ac):
        response = await ac.get("/auth/me")
        assert response.status_code == 401
