from fastapi import Request, HTTPException, status
from uuid import UUID

from backend.infrastructure.utils.security import decode_access_token


def get_current_user_id(request: Request) -> UUID:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не авторизован",
        )
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный или истёкший токен",
        )
    return UUID(payload["sub"])

