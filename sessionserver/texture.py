from fastapi import APIRouter
from response import ErrorResponse

router = APIRouter()

from mongo import db

from utils.uuid_utils import uuid_encode

from utils.serialization_profile import serialize_profile


@router.get("/session/minecraft/profile/{uuid}")
async def minecraft_profile(uuid: str, unsigned: bool = True):
    UserID = uuid_encode(uuid)

    UserData = db("users").find_one({"_id": UserID})
    if UserData is None:
        raise ErrorResponse(status_code=404, detail="User not found")

    return serialize_profile(UserData, unsigned)
