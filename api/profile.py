import requests
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response

from mongo import db
from response import ErrorResponse
from utils.uuid_utils import uuid_encode

router = APIRouter()

import re


def is_alphanumeric_underscore(input_string):
    return bool(re.match("^[A-Za-z0-9_-]*$", input_string))


@router.post("/user/profile/{uuid}/name")
async def update_profileName(request: Request, uuid: str):
    request_data = await request.json()
    accessToken = request_data["accessToken"]
    profileName = request_data["profileName"]
    if not is_alphanumeric_underscore(profileName):
        raise ErrorResponse(status_code=403, cause="The user name must consist of numeric, letters and \"_\"")

    userId = uuid_encode(uuid)

    TokenData = db("tokens").find_one({"token": accessToken, "type": "accessToken", "uid": userId})
    if TokenData is None:
        raise ErrorResponse(status_code=403, cause="No login!")
    UserData = db("users").find_one({"_id": TokenData["uid"]})
    if UserData is None:
        raise ErrorResponse(status_code=403, cause="Profile Not Found!")

    CheckLocalUser = db("users").find_one({"username": profileName})
    if CheckLocalUser:
        raise ErrorResponse(status_code=400, cause="Username is already exits!")
    CheckMojangUser = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{profileName}")
    if CheckMojangUser.ok:
        raise ErrorResponse(status_code=400, cause="Username is used by mojang server!")

    query = {"_id": UserData["_id"]}
    update = {"$set": {"username": profileName}}
    db("users").update_one(query, update)

    return Response(status_code=204)
