import time

from fastapi import APIRouter

from mongo import db
from response import ErrorResponse

router = APIRouter()
import requests, base64, json

from utils.serialization_profile import serialize_profile


@router.get("/session/minecraft/hasJoined")
async def getMinecraftHasJoined(username: str, serverId: str, ip: str = None):
    JoinData = db("joins").find_one({"username": username, "_id": serverId})
    if JoinData:
        UserData = db("users").find_one({"_id": JoinData["uid"]})

        return serialize_profile(UserData)

    request = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if request.ok:

        response = requests.get(
            url="https://sessionserver.mojang.com/session/minecraft/hasJoined",
            params={
                "username": username,
                "serverId": serverId,
                "ip": ip
            }
        )
        if response.status_code != 204:
            response = response.json()

            TexturesData = json.loads(base64.b64decode(response["properties"][0]["value"]).decode("utf-8"))
            TexturesData["timestamp"] = int(time.time() * 1000)
            if response["id"] == "46b6496f7e104a33abd168921bd4efbc":
                response["id"] = "a52dc48825554c438428-614b56790327"
                TexturesData["profileId"] = "a52dc48825554c438428-614b56790327"
                TexturesData["textures"]["CAPE"] = {}
                TexturesData["textures"]["CAPE"][
                    "url"] = "https://textures.minecraft.net/texture/bcf5cf5bfd72ac01b38bbe5030e105cc6de272b439c9623edda5db64f5e95131"
            if response["id"] == "d7b7b10f27a540e5be65069d2f6a59b9" or response['id'] == '31c93266d0de4eaa83c548576ee060da':
                TexturesData["textures"]["CAPE"] = {}
                TexturesData["textures"]["CAPE"][
                    "url"] = "http://textures.minecraft.net/texture/afd553b39358a24edfe3b8a9a939fa5fa4faa4d9a9c3d6af8eafb377fa05c2bb"
            TexturesData = json.dumps(TexturesData, indent=2)

            response["properties"][0]["value"] = base64.b64encode(str(TexturesData).encode("utf-8")).decode("utf-8")
            response["properties"][0]["signature"] = ""

            return response
    raise ErrorResponse(status_code=404)
