import re
import uuid

import requests
from fastapi import APIRouter
from fastapi.requests import Request
from response import ErrorResponse

router = APIRouter()

from mongo import db
import hashlib

from utils.serialization_profile import serialize_profile
from utils.create_token import create_token


def is_alphanumeric_underscore(input_string):
    return bool(re.match("^[A-Za-z0-9_-]*$", input_string))


@router.post("/join")
async def join(request: Request, useSHA1: bool = True):
    request_data = await request.json()

    email = request_data.get("email")
    CheckLocalEmail = db("users").find_one({"email": {"$regex": f"^{email}$", "$options": "i"}})
    if CheckLocalEmail:
        raise ErrorResponse(status_code=400, cause="Email already be register!")

    username = request_data.get("username")
    if not is_alphanumeric_underscore(username):
        raise ErrorResponse(status_code=403, cause="The user name must consist of numeric, letters and \"_\"")
    CheckLocalUser = db("users").find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
    if CheckLocalUser:
        raise ErrorResponse(status_code=400, cause="Username is already exits!")
    CheckMojangUser = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if CheckMojangUser.ok:
        raise ErrorResponse(status_code=400, cause="Username is used by mojang server!")

    password = request_data.get("password")
    if useSHA1:
        password = hashlib.sha1(password.encode())
        password = password.hexdigest()
    password = hashlib.sha256(password.encode("utf-8"))
    password = password.hexdigest()
    requestUser = request_data.get("requestUser")

    db("users").insert_one({"_id": str(uuid.uuid4()), "username": username, "email": email, "password": password, "textures": {
        "SKIN": {
            "url": "http://textures.minecraft.net/texture/6ea6a47358157ac85c050760d26f9cbae058b370811ef1927bc55009d5b81f4f",
            "metadata": {
                "model": "slim"
            }
        }
    }})

    UserData = db("users").find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})
    if UserData is None: raise ErrorResponse(status_code=403, cause="Failed to create user")

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
