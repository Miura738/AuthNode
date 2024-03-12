from datetime import datetime, timedelta

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response

from mongo import db

router = APIRouter()

from utils.uuid_utils import uuid_encode
from response import ErrorResponse


@router.post("/session/minecraft/join")
async def join_session(request: Request):
    request_data = await request.json()

    accessToken = request_data["accessToken"]
    selectedProfile = request_data["selectedProfile"]
    selectedProfile = uuid_encode(selectedProfile)
    serverId = request_data["serverId"]

    TokenData = db("tokens").find_one({"uid": selectedProfile, "token": accessToken, "type": "accessToken"})
    if TokenData is None:
        raise ErrorResponse(status_code=403, detail="请检查AccessToken是否过期")

    UserData = db("users").find_one({"_id": TokenData["uid"]})
    if UserData is None:
        raise ErrorResponse(status_code=403, detail="用户未注册/已注销")

    db("joins").create_index("expiry_time", expireAfterSeconds=30)
    db("joins").insert_one(
        {"_id": serverId, "username": UserData["username"], "uid": TokenData["uid"],
         "expiry_time": datetime.utcnow() + timedelta(seconds=30)})

    return Response(status_code=204)
