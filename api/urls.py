from fastapi import APIRouter

router = APIRouter()

from . import texture

router.include_router(texture.router, prefix="")
