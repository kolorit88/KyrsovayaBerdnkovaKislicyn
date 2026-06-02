import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.config_load import settings
from backend.db import init_redis, close_redis
from backend.infrastructure.dependencies.auth import get_auth_adapter
from backend.infrastructure.scheduling.scheduler_manager import SchedulerManager
from backend.infrastructure.scheduling.tasks.cleanup_tasks import cleanup_expired_tokens
from backend.presentation.controllers.merchandise_router import router as merchandise_router
from backend.presentation.controllers.auth_router import router as auth_router
from backend.presentation.controllers.order_router import router as order_router
from backend.presentation.controllers.user_router import router as user_router

# redis / scheduler
@asynccontextmanager
async def lifespan(app: FastAPI):
    _scheduler_manager = SchedulerManager()

    # Инициализация инфраструктуры
    await init_redis()

    # Подготовка зависимости для задачи
    auth_adapter = get_auth_adapter()

    # Планируем задачу (каждый час)
    _scheduler_manager.add_interval_job(
        func=cleanup_expired_tokens,
        job_id="cleanup_expired_refresh_tokens",
        minutes=0,
        seconds=5,
        args=(auth_adapter,)
    )
    _scheduler_manager.start()

    yield

    # Graceful shutdown
    _scheduler_manager.shutdown(wait=False)
    await close_redis()
app = FastAPI(lifespan=lifespan)
app.include_router(merchandise_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(order_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":  
    uvicorn.run("main:app", host="0.0.0.0", reload=True)