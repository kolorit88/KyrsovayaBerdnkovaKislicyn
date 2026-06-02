from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from backend.config_load import settings

_conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

_fm = FastMail(_conf)


async def send_verification_email(to_email: str, token: str) -> None:
    link = f"{settings.BACKEND_URL}/auth/verify-email?token={token}"
    body = f"""
    <h2>Подтверждение почты</h2>
    <p>Перейдите по ссылке для активации аккаунта:</p>
    <a href="{link}">{link}</a>
    <p>Ссылка действует 24 часа.</p>
    """
    message = MessageSchema(
        subject="Подтвердите вашу почту",
        recipients=[to_email],
        body=body,
        subtype=MessageType.html,
    )
    await _fm.send_message(message)


async def send_password_reset_email(to_email: str, token: str) -> None:
    link = f"{settings.FRONTEND_URL}/auth/reset-password?token={token}"
    body = f"""
    <h2>Сброс пароля</h2>
    <p>Перейдите по ссылке для сброса пароля:</p>
    <a href="{link}">{link}</a>
    <p>Ссылка действует 1 час.</p>
    <p>Если вы не запрашивали сброс — проигнорируйте это письмо.</p>
    """
    message = MessageSchema(
        subject="Сброс пароля",
        recipients=[to_email],
        body=body,
        subtype=MessageType.html,
    )
    await _fm.send_message(message)
