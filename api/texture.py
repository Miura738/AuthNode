from typing import io

from fastapi import APIRouter

from fastapi import HTTPException
from PIL import Image
import requests
import io
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.put("/user/profile/{uuid}/{textureType}")
async def update_texture(uuid: str, textureType: str):
    return {}


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
