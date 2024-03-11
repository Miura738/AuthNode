from fastapi import APIRouter

router = APIRouter()

from . import main

router.include_router(main.router, prefix="")
