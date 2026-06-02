from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status

from backend.domain.ports.auth_port import AuthPort
from backend.domain.services.auth_service_interface import AuthServiceInterface
from backend.infrastructure.utils.email_service import (
    send_verification_email,
    send_password_reset_email,
)

from backend.infrastructure.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    generate_refresh_token,
    hash_token,
    refresh_token_expires_at,
    generate_email_token,
    email_verification_expires_at,
    password_reset_expires_at,
)


class AuthService(AuthServiceInterface):

    def __init__(self, auth_adapter: AuthPort):
        self._adapter = auth_adapter

    # ------------------------------------------------------------------ #
    #  Регистрация                                                         #
    # ------------------------------------------------------------------ #

    async def register(
            self, name: str, email: str, phone_number: str, address: str, password: str
    ) -> dict:

        existing = await self._adapter.get_user_by_email(email)

        if existing:
            if existing.is_active:
                raise HTTPException(status_code=409, detail="Email уже занят")

            # Пользователь есть, но не активирован — перевыпускаем токен
            token = generate_email_token()
            await self._adapter.delete_email_verification_tokens(existing.id)
            await self._adapter.create_email_verification_token(
                user_id=existing.id,
                token=token,
                expires_at=email_verification_expires_at(),
            )
            await send_verification_email(email, token)
            return {"message": "Письмо отправлено повторно. Проверьте почту."} # сделать DTO

        if await self._adapter.get_user_by_email(email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким email уже существует",
            )
        if await self._adapter.get_user_by_phone(phone_number):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким номером телефона уже существует",
            )

        user = await self._adapter.create_user(
            name=name,
            email=email,
            phone_number=phone_number,
            address=address,
            hashed_password=hash_password(password),
        )

        token = generate_email_token()
        await self._adapter.create_email_verification_token(
            user_id=user.id,
            token=token,
            expires_at=email_verification_expires_at(),
        )
        await send_verification_email(email, token)

        return {"message": "Регистрация прошла успешно. Проверьте почту для подтверждения."} # сделать DTO

    # ------------------------------------------------------------------ #
    #  Подтверждение почты                                                 #
    # ------------------------------------------------------------------ #

    async def verify_email(self, token: str) -> dict:
        record = await self._adapter.get_email_verification_token(token)

        if not record:
            raise HTTPException(status_code=400, detail="Недействительная ссылка")
        if record["used"]:
            raise HTTPException(status_code=400, detail="Ссылка уже использована")
        if record["expires_at"] < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Ссылка истекла")

        await self._adapter.mark_email_token_used(token)
        user = await self._adapter.update_user(record["user_id"], is_active=True)

        # Сразу логиним пользователя
        access_token = create_access_token(user.id, user.role.value)
        refresh_token_raw = generate_refresh_token()
        await self._adapter.save_refresh_token(
            user_id=user.id,
            token_hash=hash_token(refresh_token_raw),
            expires_at=refresh_token_expires_at(),
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token_raw,
            "token_type": "bearer",
        }

    # ------------------------------------------------------------------ #
    #  Вход                                                                #
    # ------------------------------------------------------------------ #

    async def login(self, login: str, password: str) -> dict:
        # Поддерживаем вход по email
        user = await self._adapter.get_user_by_email(login)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Аккаунт не активирован. Проверьте почту.",
            )

        access_token = create_access_token(user.id, user.role.value)
        refresh_token_raw = generate_refresh_token()
        token_hash = hash_token(refresh_token_raw)

        await self._adapter.save_refresh_token(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=refresh_token_expires_at(),
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token_raw,
            "token_type": "bearer",
        }

    # ------------------------------------------------------------------ #
    #  Выход                                                               #
    # ------------------------------------------------------------------ #

    async def logout(self, refresh_token: str) -> None:
        token_hash = hash_token(refresh_token)
        record = await self._adapter.get_refresh_token(token_hash)
        if record:
            await self._adapter.revoke_refresh_token(token_hash)

    # ------------------------------------------------------------------ #
    #  Обновление токенов                                                  #
    # ------------------------------------------------------------------ #

    async def refresh_tokens(self, refresh_token: str) -> dict:
        token_hash = hash_token(refresh_token)
        record = await self._adapter.get_refresh_token(token_hash)

        if not record:
            raise HTTPException(status_code=401, detail="Refresh-токен не найден")
        if record["revoked"]:
            # Возможная атака — инвалидируем все токены пользователя
            await self._adapter.revoke_all_user_refresh_tokens(record["user_id"])
            raise HTTPException(status_code=401, detail="Токен отозван. Войдите заново.")
        if record["expires_at"] < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Refresh-токен истёк")

        user = await self._adapter.get_user_by_id(record["user_id"])
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="Пользователь недоступен")

        await self._adapter.revoke_refresh_token(token_hash)
        new_refresh_raw = generate_refresh_token()
        new_hash = hash_token(new_refresh_raw)
        await self._adapter.save_refresh_token(
            user_id=user.id,
            token_hash=new_hash,
            expires_at=refresh_token_expires_at(),
        )

        return {
            "access_token": create_access_token(user.id, user.role.value),
            "refresh_token": new_refresh_raw,
            "token_type": "bearer",
        }

    # ------------------------------------------------------------------ #
    #  Профиль                                                             #
    # ------------------------------------------------------------------ #

    async def get_me(self, user_id: UUID) -> dict:
        user = await self._adapter.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        return {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number,
            "address": user.address,
            "role": user.role.value,
            "is_active": user.is_active,
            "created_at": user.created_at,
        }

    async def update_me(self, user_id: UUID, **fields) -> dict:
        # Проверка уникальности email/телефона если они меняются
        if "email" in fields:
            existing = await self._adapter.get_user_by_email(fields["email"])
            if existing and existing.id != user_id:
                raise HTTPException(status_code=409, detail="Email уже занят")
        if "phone_number" in fields:
            existing = await self._adapter.get_user_by_phone(fields["phone_number"])
            if existing and existing.id != user_id:
                raise HTTPException(status_code=409, detail="Телефон уже занят")

        user = await self._adapter.update_user(user_id, **fields)
        return await self.get_me(user_id)

    # ------------------------------------------------------------------ #
    #  Смена и сброс пароля                                               #
    # ------------------------------------------------------------------ #

    async def change_password(
            self, user_id: UUID, old_password: str, new_password: str
    ) -> None:
        user = await self._adapter.get_user_by_id(user_id)
        if not user or not verify_password(old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Неверный текущий пароль")

        await self._adapter.update_user(
            user_id, hashed_password=hash_password(new_password)
        )
        # Инвалидируем все refresh-токены (смена пароля = выход со всех устройств)
        await self._adapter.revoke_all_user_refresh_tokens(user_id)

    async def request_password_reset(self, email: str) -> None:
        user = await self._adapter.get_user_by_email(email)
        # Не раскрываем наличие/отсутствие аккаунта
        if not user:
            return

        token = generate_email_token()
        await self._adapter.create_password_reset_token(
            user_id=user.id,
            token=token,
            expires_at=password_reset_expires_at(),
        )
        await send_password_reset_email(email, token)

    async def reset_password(self, token: str, new_password: str) -> None:
        record = await self._adapter.get_password_reset_token(token)

        if not record:
            raise HTTPException(status_code=400, detail="Недействительная ссылка")
        if record["used"]:
            raise HTTPException(status_code=400, detail="Ссылка уже использована")
        if record["expires_at"] < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Ссылка истекла")

        await self._adapter.mark_password_reset_token_used(token)
        await self._adapter.update_user(
            record["user_id"], hashed_password=hash_password(new_password)
        )
        await self._adapter.revoke_all_user_refresh_tokens(record["user_id"])