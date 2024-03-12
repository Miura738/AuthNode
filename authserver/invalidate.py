from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response
from response import ErrorResponse

router = APIRouter()

from mongo import db


@router.post("")
async def invalidate(request: Request):
    request_data = await request.json()

    accessToken = request_data.get("accessToken")

    TokenData = db("tokens").find_one({"token": accessToken, "type": "accessToken"})
    if TokenData:
        db("tokens").delete_one({"_id": TokenData["_id"]})
    return Response(status_code=204)
