"""
Unit-тесты для AuthService.

Все зависимости (AuthPort) мокаются — БД не нужна.
Запуск: pytest tests/unit/test_auth_service.py -v
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from backend.application.services.auth_service import AuthService
from backend.domain.models.user import User
from backend.domain.values import Role


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def make_user(**kwargs) -> User:
    defaults = dict(
        id=uuid4(),
        name="Иван Иванов",
        email="ivan@example.com",
        phone_number="+79001234567",
        address="Москва, ул. Пушкина, 1",
        hashed_password="hashed_secret",
        is_active=True,
        role=Role.USER,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    defaults.update(kwargs)
    return User(**defaults)


def make_auth_adapter(**overrides) -> AsyncMock:
    """Возвращает мок AuthPort с разумными дефолтами."""
    adapter = AsyncMock()
    adapter.get_user_by_email.return_value = None
    adapter.get_user_by_phone.return_value = None
    adapter.create_user.return_value = make_user()
    adapter.create_email_verification_token.return_value = None
    adapter.delete_email_verification_tokens.return_value = None
    for attr, val in overrides.items():
        setattr(adapter, attr, val)
    return adapter


# ─────────────────────────────────────────────
# register()
# ─────────────────────────────────────────────

class TestRegister:
    @pytest.mark.asyncio
    async def test_register_new_user_sends_email(self):
        """При регистрации нового пользователя отправляется письмо подтверждения."""
        adapter = make_auth_adapter()
        service = AuthService(adapter)

        with patch("backend.application.services.auth_service.send_verification_email") as mock_send:
            result = await service.register(
                name="Иван",
                email="ivan@example.com",
                phone_number="+79001234567",
                address="Москва",
                password="strongpass123",
            )

        adapter.create_user.assert_awaited_once()
        adapter.create_email_verification_token.assert_awaited_once()
        mock_send.assert_awaited_once()
        assert "message" in result

    @pytest.mark.asyncio
    async def test_register_duplicate_active_email_raises_409(self):
        """Регистрация с уже занятым активным email → HTTP 409."""
        from fastapi import HTTPException

        existing = make_user(is_active=True)
        adapter = make_auth_adapter()
        adapter.get_user_by_email.return_value = existing
        service = AuthService(adapter)

        with pytest.raises(HTTPException) as exc_info:
            await service.register(
                name="Другой",
                email="ivan@example.com",
                phone_number="+79009999999",
                address="СПб",
                password="strongpass123",
            )

        assert exc_info.value.status_code == 409

    @pytest.mark.asyncio
    async def test_register_inactive_user_resends_verification(self):
        """Если пользователь есть, но не активирован — перевыпускаем токен."""
        inactive = make_user(is_active=False)
        adapter = make_auth_adapter()
        adapter.get_user_by_email.return_value = inactive
        service = AuthService(adapter)

        with patch("backend.application.services.auth_service.send_verification_email") as mock_send:
            result = await service.register(
                name="Иван",
                email="ivan@example.com",
                phone_number="+79001234567",
                address="Москва",
                password="strongpass123",
            )

        adapter.delete_email_verification_tokens.assert_awaited_once_with(inactive.id)
        adapter.create_email_verification_token.assert_awaited_once()
        mock_send.assert_awaited_once()
        assert "message" in result


# ─────────────────────────────────────────────
# login()
# ─────────────────────────────────────────────

class TestLogin:
    @pytest.mark.asyncio
    async def test_login_success_returns_tokens(self):
        """Корректные учётные данные → возвращаются access и refresh токены."""
        user = make_user(is_active=True)
        adapter = make_auth_adapter()
        adapter.get_user_by_email.return_value = user
        adapter.save_refresh_token.return_value = None
        service = AuthService(adapter)

        with patch("backend.application.services.auth_service.verify_password", return_value=True):
            result = await service.login(login="ivan@example.com", password="correct")

        assert "access_token" in result
        assert "refresh_token" in result
        assert result["token_type"] == "bearer"
        adapter.save_refresh_token.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_login_wrong_password_raises_401(self):
        """Неверный пароль → HTTP 401."""
        from fastapi import HTTPException

        user = make_user(is_active=True)
        adapter = make_auth_adapter()
        adapter.get_user_by_email.return_value = user
        service = AuthService(adapter)

        with patch("backend.application.services.auth_service.verify_password", return_value=False):
            with pytest.raises(HTTPException) as exc_info:
                await service.login(login="ivan@example.com", password="wrong")

        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_login_inactive_user_raises_403(self):
        """Неактивный аккаунт → HTTP 403."""
        from fastapi import HTTPException

        user = make_user(is_active=False)
        adapter = make_auth_adapter()
        adapter.get_user_by_email.return_value = user
        service = AuthService(adapter)

        with patch("backend.application.services.auth_service.verify_password", return_value=True):
            with pytest.raises(HTTPException) as exc_info:
                await service.login(login="ivan@example.com", password="correct")

        assert exc_info.value.status_code == 403


# ─────────────────────────────────────────────
# refresh_tokens()
# ─────────────────────────────────────────────

class TestRefreshTokens:
    def _make_token_record(self, revoked=False, expired=False):
        user_id = uuid4()
        expires_at = (
            datetime.utcnow() - timedelta(hours=1)
            if expired
            else datetime.utcnow() + timedelta(days=7)
        )
        return {"user_id": user_id, "expires_at": expires_at, "revoked": revoked}

    @pytest.mark.asyncio
    async def test_refresh_revoked_token_revokes_all_and_raises_401(self):
        """Попытка использовать отозванный токен → инвалидируем все токены пользователя."""
        from fastapi import HTTPException

        record = self._make_token_record(revoked=True)
        adapter = make_auth_adapter()
        adapter.get_refresh_token.return_value = record
        service = AuthService(adapter)

        with pytest.raises(HTTPException) as exc_info:
            await service.refresh_tokens("some_revoked_token")

        adapter.revoke_all_user_refresh_tokens.assert_awaited_once_with(record["user_id"])
        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_refresh_expired_token_raises_401(self):
        """Истёкший токен → HTTP 401."""
        from fastapi import HTTPException

        record = self._make_token_record(expired=True)
        adapter = make_auth_adapter()
        adapter.get_refresh_token.return_value = record
        service = AuthService(adapter)

        with pytest.raises(HTTPException) as exc_info:
            await service.refresh_tokens("expired_token")

        assert exc_info.value.status_code == 401