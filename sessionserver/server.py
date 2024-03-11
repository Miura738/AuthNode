import time

from fastapi import APIRouter

from response import ErrorResponse

router = APIRouter()
import requests, base64, json


@router.get("/session/minecraft/hasJoined")
async def getMinecraftHasJoined(username: str, serverId: str, ip: str = None):

    request = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if request.ok:

        response = requests.get(
            url="https://sessionserver.mojang.com/session/minecraft/hasJoined",
            params={
                "username": username,
                "serverId": serverId,
                "ip": ip
            }
        ).json()

        TexturesData = json.loads(base64.b64decode(response["properties"][0]["value"]).decode("utf-8"))
        TexturesData["timestamp"] = int(time.time() * 1000)
        if response["id"] == "46b6496f7e104a33abd168921bd4efbc":
            TexturesData["textures"]["CAPE"] = {}
            TexturesData["textures"]["CAPE"][
                "url"] = "http://textures.minecraft.net/texture/2340c0e03dd24a11b15a8b33c2a7e9e32abb2051b2481d0ba7defd635ca7a933"
        if response["id"] == "d7b7b10f27a540e5be65069d2f6a59b9" or response['id'] == '31c93266d0de4eaa83c548576ee060da':
            TexturesData["textures"]["CAPE"] = {}
            TexturesData["textures"]["CAPE"][
                "url"] = "http://textures.minecraft.net/texture/afd553b39358a24edfe3b8a9a939fa5fa4faa4d9a9c3d6af8eafb377fa05c2bb"
        TexturesData = json.dumps(TexturesData, indent=2)

        response["properties"][0]["value"] = base64.b64encode(str(TexturesData).encode("utf-8")).decode("utf-8")
        response["properties"][0]["signature"] = ""

        return response
    else:
        raise ErrorResponse(status_code=404)
