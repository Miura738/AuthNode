from fastapi import APIRouter

from response import ErrorResponse

router = APIRouter()


@router.put("/user/profile/{uuid}/{textureType}")
async def update_texture(uuid: str, textureType: str):
    return {}
