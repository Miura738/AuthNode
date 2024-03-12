from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response
from response import ErrorResponse

router = APIRouter()

from mongo import db


@router.post("")
async def validate(request: Request):
    request_data = await request.json()

    accessToken = request_data.get("accessToken")

    TokenData = db("tokens").find_one({"token": accessToken, "type": "accessToken"})
    if TokenData is None:
        return ErrorResponse(status_code=403)

    return Response(status_code=204)
