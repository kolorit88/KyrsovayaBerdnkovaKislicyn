from fastapi import Response
from backend.config_load import settings


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    """Устанавливает httpOnly-куки для access и refresh токенов."""
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
    )


def delete_auth_cookies(response: Response) -> None:
    """Удаляет куки access и refresh токенов."""
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token", path="/auth/refresh")
