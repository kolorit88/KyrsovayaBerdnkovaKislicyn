from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as async_redis

from backend.config_load import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

redis_client = None

async def init_redis() -> None:
    """Инициализация подключения к Redis."""
    global redis_client
    # Используйте ваш URL или параметры подключения
    redis_client = await async_redis.from_url(
        settings.REDIS_URL,
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(
        RedisBackend(redis_client),
        prefix="fastapi-cache"
    )

async def close_redis() -> None:
    """Закрытие соединения с Redis."""
    if redis_client is not None:
        await redis_client.close()