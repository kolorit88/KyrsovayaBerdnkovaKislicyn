import logging
from backend.domain.ports.auth_port import AuthPort

logger = logging.getLogger(__name__)

async def cleanup_expired_tokens(auth_adapter: AuthPort) -> None:
    """
    Фоновая задача очистки истёкших refresh-токенов.
    Вызывается планировщиком.
    """
    try:
        deleted = await auth_adapter.delete_expired_refresh_tokens()
        if deleted:
            logger.info(f"Удалено {deleted} истёкших refresh-токенов")
        elif deleted == 0:
            logger.debug("Нет истёкших refresh-токенов для удаления")
    except Exception as e:
        logger.exception("Ошибка при очистке refresh-токенов: %s", e)