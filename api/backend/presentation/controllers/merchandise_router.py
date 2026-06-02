import asyncio

from fastapi import Depends, APIRouter
from fastapi_cache.decorator import cache
from backend.infrastructure.dependencies.merchandise import get_merchandise_service
from backend.application.services.merchandise_service import MerchandiseService

router = APIRouter()

@router.get("/merchandise")
@cache(expire=60*10)
async def get_all_merchandise(
    service: MerchandiseService = Depends(get_merchandise_service)
):
    return await service.get_all_merchandise_divided_into_categories()