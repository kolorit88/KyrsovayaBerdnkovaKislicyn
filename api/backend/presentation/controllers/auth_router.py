from fastapi import APIRouter, Depends, HTTPException, Request, Response

from backend.application.services.auth_service import AuthService
from backend.infrastructure.dependencies.auth import get_auth_service
from backend.infrastructure.dto.auth_dto import (
    RegisterRequest,
    LoginRequest,
    VerifyEmailRequest,
    TokenResponse,
    MessageResponse,
)
from backend.infrastructure.utils.cookie_helper import set_auth_cookies, delete_auth_cookies

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=MessageResponse, status_code=201)
async def register(
    body: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    """Регистрация. Отправляет письмо с подтверждением на почту."""
    return await service.register(
        name=body.name,
        email=body.email,
        phone_number=body.phone_number,
        address=body.address,
        password=body.password,
    )


@router.get("/verify-email", response_model=MessageResponse)
async def verify_email(
    response: Response,
    token: str,
    service: AuthService = Depends(get_auth_service),
):
    tokens = await service.verify_email(token)
    set_auth_cookies(response, tokens["access_token"], tokens["refresh_token"])
    return {"message": "Email подтверждён, вы вошли в систему"}


@router.post("/login", response_model=MessageResponse)
async def login(
    response: Response,
    body: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    tokens = await service.login(login=body.login, password=body.password)
    set_auth_cookies(response, tokens["access_token"], tokens["refresh_token"])
    return {"message": "Вход выполнен успешно"}


@router.post("/refresh", response_model=MessageResponse)
async def refresh(
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh-токен отсутствует")

    tokens = await service.refresh_tokens(refresh_token)
    set_auth_cookies(response, tokens["access_token"], tokens["refresh_token"])
    return {"message": "Токены обновлены"}


@router.post("/logout", response_model=MessageResponse)
async def logout(
    request: Request,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        await service.logout(refresh_token)

    delete_auth_cookies(response)
    return {"message": "Вы вышли из системы"}
