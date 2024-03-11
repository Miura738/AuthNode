

from fastapi import APIRouter

from response import ErrorResponse

router = APIRouter()


@router.get("/authenticate")
@router.post("/authenticate")
async def authenticate():
    raise ErrorResponse(status_code=403, cause="此邮箱未注册",errorMessage="你好")
