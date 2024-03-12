from fastapi import APIRouter

router = APIRouter()

from . import texture,profile

router.include_router(profile.router, prefix="")
router.include_router(texture.router, prefix="")
