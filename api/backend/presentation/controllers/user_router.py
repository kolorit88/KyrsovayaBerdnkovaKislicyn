from uuid import UUID

from fastapi import APIRouter, Depends, Response
from backend.application.services.auth_service import AuthService
from backend.infrastructure.dependencies.auth import get_auth_service
from backend.infrastructure.dependencies.current_user import get_current_user_id
from backend.infrastructure.dto.auth_dto import (
    UpdateMeRequest,
    ChangePasswordRequest,
    RequestPasswordResetRequest,
    ResetPasswordRequest,
    UserResponse,
    MessageResponse,
)
from backend.infrastructure.utils.cookie_helper import delete_auth_cookies

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_me(
    user_id: UUID = Depends(get_current_user_id),
    service: AuthService = Depends(get_auth_service),
):
    """Получить профиль текущего пользователя."""
    return await service.get_me(user_id)


@router.patch("/me", response_model=UserResponse)
async def update_me(
    body: UpdateMeRequest,
    user_id: UUID = Depends(get_current_user_id),
    service: AuthService = Depends(get_auth_service),
):
    """Обновить имя, телефон или адрес."""
    fields = body.model_dump(exclude_none=True)
    return await service.update_me(user_id, **fields)


@router.post("/me/password/change", response_model=MessageResponse)
async def change_password(
    response: Response,
    body: ChangePasswordRequest,
    user_id: UUID = Depends(get_current_user_id),
    service: AuthService = Depends(get_auth_service),
):
    await service.change_password(user_id, body.old_password, body.new_password)
    delete_auth_cookies(response)
    return {"message": "Пароль изменён. Войдите заново."}


@router.post("/me/reset-password", response_model=MessageResponse)
async def request_password_reset(
    body: RequestPasswordResetRequest,
    service: AuthService = Depends(get_auth_service),
):
    """Запрос сброса пароля — отправляет письмо на указанный email."""
    await service.request_password_reset(body.email)
    return {"message": "Если аккаунт существует, письмо отправлено"}


@router.post("/me/reset-password/confirm", response_model=MessageResponse)
async def reset_password(
    response: Response,
    body: ResetPasswordRequest,
    service: AuthService = Depends(get_auth_service),
):
    """Подтверждение сброса пароля по токену из письма."""
    await service.reset_password(body.token, body.new_password)
    delete_auth_cookies(response)
    return {"message": "Пароль успешно сброшен"}
