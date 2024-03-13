import base64
import json

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi import HTTPException
from PIL import Image
import requests
import io
from fastapi.responses import StreamingResponse

from mongo import db
from response import ErrorResponse
from utils.serialization_profile import serialize_profile
from utils.uuid_utils import uuid_encode

router = APIRouter()


@router.put("/user/profile/{uuid}/{textureType}")
async def update_texture(request: Request, uuid: str, textureType: str, model: str = Form(""),
                         file: UploadFile = File(...), backTextures: bool = False):
    if textureType == "SKIN":

        accessToken = request.headers.get("Authorization").split(" ")[-1]

        userId = uuid_encode(uuid)
        TokenData = db("tokens").find_one({"token": accessToken, "type": "accessToken", "uid": userId})
        if TokenData is None:
            raise ErrorResponse(status_code=403, cause="No login!")
        UserData = db("users").find_one({"_id": TokenData["uid"]})
        if UserData is None:
            raise ErrorResponse(status_code=403, cause="Profile Not Found!")

        skinType = model
        if skinType is None:
            skinType = ""
        skinFile = await file.read()

        if file.content_type != "image/png":
            raise ErrorResponse(status_code=400, cause=f"File type error!")
        image = Image.open(io.BytesIO(skinFile))
        width, height = image.size
        if (width == 64 and height == 64) or (width == 64 and height == 32):
            pass
        else:
            raise ErrorResponse(status_code=400, cause=f"File type error!")

        uuid = "f35d03609f004c80acf1e1452377546a"
        access_token = "eyJraWQiOiJhYzg0YSIsImFsZyI6IkhTMjU2In0.eyJ4dWlkIjoiMjUzNTQ2NDg5MjQ2ODI2NiIsImFnZyI6IkFkdWx0Iiwic3ViIjoiYmU3OGNlOTItM2E3Ni00NDY1LWEzYzktODRhOTUwNGFjYTI3IiwiYXV0aCI6IlhCT1giLCJucyI6ImRlZmF1bHQiLCJyb2xlcyI6W10sImlzcyI6ImF1dGhlbnRpY2F0aW9uIiwiZmxhZ3MiOlsidHdvZmFjdG9yYXV0aCIsIm1zYW1pZ3JhdGlvbl9zdGFnZTQiLCJvcmRlcnNfMjAyMiIsIm11bHRpcGxheWVyIl0sInByb2ZpbGVzIjp7Im1jIjoiZjM1ZDAzNjAtOWYwMC00YzgwLWFjZjEtZTE0NTIzNzc1NDZhIn0sInBsYXRmb3JtIjoiVU5LTk9XTiIsInl1aWQiOiI3N2ExYzA1Mjg5Njc4N2MzYzkzMjk2NGFkNjM5YzM1MyIsIm5iZiI6MTcxMDI4NTIzOSwiZXhwIjoxNzEwMzcxNjM5LCJpYXQiOjE3MTAyODUyMzl9.CuaVLlJ60Tyo9X4i1PPDXwwObhtGI-dt7mpkyDg3VKA"

        # 构建请求URL和头部信息
        url = f"https://api.minecraftservices.com/minecraft/profile/skins"
        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        # 发起请求，并上传皮肤
        response = requests.post(url, headers=headers, data={
            "variant": skinType,
        }, files={
            'file': (file.filename, skinFile, 'image/png')
        })
        if response.ok:
            request_skin = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
            if request_skin.ok:
                request_skin = request_skin.json()
                texturesJSON = json.loads(base64.b64decode(request_skin["properties"][0]["value"]).decode("utf-8"))

                db("users").update_one({'_id': UserData["_id"]},
                                       {'$set': {'textures.SKIN': texturesJSON["textures"]["SKIN"]}})
                UserData = db("users").find_one({"_id": UserData["_id"]})

                if backTextures:
                    return serialize_profile(UserData)
                return Response(status_code=204)

        raise ErrorResponse(status_code=400, cause="Mojang server error!")

    raise ErrorResponse(status_code=404, cause="textures Type Not Found!")


def process_image(image_url):
    try:
        response = requests.get(image_url)
        image = Image.open(io.BytesIO(response.content))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to fetch or process the image")

    # 裁剪底部内容
    bottom_content = image.crop((8, 8, 16, 16))
    bottom_content = bottom_content.resize((bottom_content.width * 7, bottom_content.height * 7),
                                           resample=Image.NEAREST)

    # 裁剪顶部内容
    top_content = image.crop((40, 8, 48, 16))
    top_content = top_content.resize((top_content.width * 8, top_content.height * 8),
                                     resample=Image.NEAREST)

    # 创建一个新的16x16大小的图片
    new_image = Image.new('RGBA', (64, 64))

    # 将底部内容粘贴到新图片的左半部分
    new_image.paste(bottom_content, (4, 4))

    # 将顶部内容粘贴到新图片的右半部分
    new_image.paste(top_content, (0, 0), mask=top_content)

    return new_image


@router.get("/parse/skin")
async def parse_skin(url: str):
    processed_image = process_image(url)

    # Convert the image to bytes
    img_byte_array = io.BytesIO()
    processed_image.save(img_byte_array, format="PNG")
    img_byte_array = img_byte_array.getvalue()

    # Return the image as response
    return StreamingResponse(io.BytesIO(img_byte_array), media_type="image/png")
