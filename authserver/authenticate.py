from fastapi import APIRouter
from fastapi.requests import Request
from response import ErrorResponse

router = APIRouter()

from mongo import db
import hashlib

from utils.serialization_profile import serialize_profile
from utils.create_token import create_token


@router.post("")
async def authenticate(request: Request, useSHA1: bool = True):
    request_data = await request.json()

    username = request_data.get("username")
    password = request_data.get("password")
    if useSHA1:
        password = hashlib.sha1(password.encode())
        password = password.hexdigest()
    password = hashlib.sha256(password.encode("utf-8"))
    password = password.hexdigest()
    requestUser = request_data.get("requestUser")

    UserData = db("users").find_one({"email": {"$regex": f"^{username}$", "$options": "i"}})
    if UserData is None: UserData = db("users").find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
    if UserData is None: raise ErrorResponse(status_code=403, cause="Unknow email or username")
    if str(UserData["password"]) != password: raise ErrorResponse(status_code=403, cause="Password error")

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
