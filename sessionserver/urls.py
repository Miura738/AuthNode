from fastapi import APIRouter

router = APIRouter()

from . import server, texture, client

router.include_router(server.router, prefix="")
router.include_router(texture.router, prefix="")
router.include_router(client.router, prefix="")
