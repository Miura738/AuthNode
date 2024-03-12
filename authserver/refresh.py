from fastapi import APIRouter
from fastapi.requests import Request
from response import ErrorResponse

router = APIRouter()

from mongo import db

from utils.serialization_profile import serialize_profile
from utils.create_token import create_token


@router.post("")
async def refresh(request: Request):
    request_data = await request.json()

    accessToken = request_data.get("accessToken")
    requestUser = request_data.get("requestUser")

    TokenData = db("tokens").find_one({"token": accessToken, "type": "accessToken"})
    if TokenData is None:
        return ErrorResponse(status_code=403)
    db("tokens").delete_one({"_id": TokenData["_id"]})
    UserData = db("users").find_one({"_id": TokenData["uid"]})

    UserProfile = serialize_profile(UserData)

    result = {
        "accessToken": create_token(UserData),
        "clientToken": None,
        "availableProfiles": [
            UserProfile
        ],
        "selectedProfile": UserProfile,
    }
    if requestUser:
        result["user"] = UserProfile

    return result
