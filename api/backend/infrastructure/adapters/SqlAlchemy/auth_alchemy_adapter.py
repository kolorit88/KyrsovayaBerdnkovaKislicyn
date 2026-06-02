from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select, update, delete

from backend.db import async_session_maker
from backend.db.models.base import Base
from backend.db.models.user import User as UserORM
from backend.db.models.refresh_token import RefreshToken as RefreshTokenORM
from backend.db.models.email_verification_token import EmailVerificationToken as EmailVerificationTokenORM
from backend.db.models.password_reset_token import PasswordResetToken as PasswordResetTokenORM
from backend.domain.models.user import User as UserDomain
from backend.domain.ports.auth_port import AuthPort
from backend.domain.values import Role


class AuthAdapterSQLAlchemy(AuthPort):

    # ------------------------------------------------------------------ #
    #  User                                                                #
    # ------------------------------------------------------------------ #

    async def get_user_by_email(self, email: str) -> Optional[UserDomain]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(UserORM).where(UserORM.email == email)
            )
            orm = result.scalar_one_or_none()
            return self._orm_to_domain(orm) if orm else None

    async def get_user_by_phone(self, phone_number: str) -> Optional[UserDomain]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(UserORM).where(UserORM.phone_number == phone_number)
            )
            orm = result.scalar_one_or_none()
            return self._orm_to_domain(orm) if orm else None

    async def get_user_by_id(self, user_id: UUID) -> Optional[UserDomain]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(UserORM).where(UserORM.id == user_id)
            )
            orm = result.scalar_one_or_none()
            return self._orm_to_domain(orm) if orm else None

    async def create_user(
        self,
        name: str,
        email: str,
        phone_number: str,
        address: str,
        hashed_password: str,
    ) -> UserDomain:
        async with async_session_maker() as session:
            orm = UserORM(
                name=name,
                email=email,
                phone_number=phone_number,
                address=address,
                hashed_password=hashed_password,
                is_active=False,  # активируется после подтверждения почты
                role=Role.USER,
            )
            session.add(orm)
            await session.commit()
            await session.refresh(orm)
            return self._orm_to_domain(orm)

    async def update_user(self, user_id: UUID, **fields) -> UserDomain:
        async with async_session_maker() as session:
            fields["updated_at"] = datetime.utcnow()
            await session.execute(
                update(UserORM).where(UserORM.id == user_id).values(**fields)
            )
            await session.commit()
            result = await session.execute(select(UserORM).where(UserORM.id == user_id))
            return self._orm_to_domain(result.scalar_one())

    # ------------------------------------------------------------------ #
    #  Email verification                                                  #
    # ------------------------------------------------------------------ #

    async def create_email_verification_token(
        self, user_id: UUID, token: str, expires_at: datetime
    ) -> None:
        async with async_session_maker() as session:
            orm = EmailVerificationTokenORM(
                user_id=user_id,
                token=token,
                expires_at=expires_at,
            )
            session.add(orm)
            await session.commit()

    async def get_email_verification_token(self, token: str) -> Optional[dict]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(EmailVerificationTokenORM).where(
                    EmailVerificationTokenORM.token == token
                )
            )
            orm = result.scalar_one_or_none()
            if not orm:
                return None
            return {"user_id": orm.user_id, "expires_at": orm.expires_at, "used": orm.used}

    async def mark_email_token_used(self, token: str) -> None:
        async with async_session_maker() as session:
            await session.execute(
                update(EmailVerificationTokenORM)
                .where(EmailVerificationTokenORM.token == token)
                .values(used=True)
            )
            await session.commit()

    # ------------------------------------------------------------------ #
    #  Password reset                                                      #
    # ------------------------------------------------------------------ #

    async def create_password_reset_token(
        self, user_id: UUID, token: str, expires_at: datetime
    ) -> None:
        async with async_session_maker() as session:
            orm = PasswordResetTokenORM(
                user_id=user_id,
                token=token,
                expires_at=expires_at,
            )
            session.add(orm)
            await session.commit()

    async def get_password_reset_token(self, token: str) -> Optional[dict]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(PasswordResetTokenORM).where(
                    PasswordResetTokenORM.token == token
                )
            )
            orm = result.scalar_one_or_none()
            if not orm:
                return None
            return {"user_id": orm.user_id, "expires_at": orm.expires_at, "used": orm.used}

    async def mark_password_reset_token_used(self, token: str) -> None:
        async with async_session_maker() as session:
            await session.execute(
                update(PasswordResetTokenORM)
                .where(PasswordResetTokenORM.token == token)
                .values(used=True)
            )
            await session.commit()

    # ------------------------------------------------------------------ #
    #  Refresh tokens                                                      #
    # ------------------------------------------------------------------ #

    async def save_refresh_token(
        self, user_id: UUID, token_hash: str, expires_at: datetime
    ) -> None:
        async with async_session_maker() as session:
            orm = RefreshTokenORM(
                user_id=user_id,
                token_hash=token_hash,
                expires_at=expires_at,
            )
            session.add(orm)
            await session.commit()

    async def get_refresh_token(self, token_hash: str) -> Optional[dict]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(RefreshTokenORM).where(
                    RefreshTokenORM.token_hash == token_hash
                )
            )
            orm = result.scalar_one_or_none()
            if not orm:
                return None
            return {
                "user_id": orm.user_id,
                "expires_at": orm.expires_at,
                "revoked": orm.revoked,
            }

    async def revoke_refresh_token(self, token_hash: str) -> None:
        async with async_session_maker() as session:
            await session.execute(
                update(RefreshTokenORM)
                .where(RefreshTokenORM.token_hash == token_hash)
                .values(revoked=True)
            )
            await session.commit()

    async def revoke_all_user_refresh_tokens(self, user_id: UUID) -> None:
        async with async_session_maker() as session:
            await session.execute(
                update(RefreshTokenORM)
                .where(RefreshTokenORM.user_id == user_id)
                .values(revoked=True)
            )
            await session.commit()

    async def delete_email_verification_tokens(self, user_id: UUID) -> None:
        async with async_session_maker() as session:
            await session.execute(
                delete(EmailVerificationTokenORM)
                .where(EmailVerificationTokenORM.user_id == user_id)
            )
            await session.commit()

    async def delete_expired_refresh_tokens(self) -> int:
        async with async_session_maker() as session:
            result = await session.execute(
                delete(RefreshTokenORM).where(RefreshTokenORM.revoked == True)
            )
            await session.commit()
            return result.rowcount

    # ------------------------------------------------------------------ #
    #  Internal mapper                                                     #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _orm_to_domain(orm: UserORM) -> UserDomain:
        return UserDomain(
            id=orm.id,
            name=orm.name,
            email=orm.email,
            phone_number=orm.phone_number,
            address=orm.address,
            hashed_password=orm.hashed_password,
            is_active=orm.is_active,
            role=orm.role,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
