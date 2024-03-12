from fastapi import APIRouter

router = APIRouter()

from . import authenticate, refresh, validate

router.include_router(authenticate.router, prefix="/authenticate")
router.include_router(refresh.router, prefix="/refresh")
router.include_router(validate.router, prefix="/validate")
