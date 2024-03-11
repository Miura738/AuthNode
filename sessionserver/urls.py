from fastapi import APIRouter

router = APIRouter()

from . import server

router.include_router(server.router, prefix="")
