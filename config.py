
class Config(object):
    MONGO_URI = "mongodb://localhost:27017/"
    MONGO_DBNAME = "AuthNode"
    MONGO_PREFIX = "an_"













from fastapi import FastAPI
from response import ErrorResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


def init(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            {
                "error": exc.status_code,
                "errorMessage": exc.detail,
            }
            , status_code=exc.status_code
        )

    @app.exception_handler(ErrorResponse)
    async def unicorn_exception_handler(request, exc: ErrorResponse):
        api = {"errorMessage": exc.detail, "error": exc.errorCode}
        if exc.errorMessage:
            api["errorMessage"] = exc.errorMessage
        if exc.cause:
            api["cause"] = exc.cause
        return JSONResponse(api, status_code=exc.status_code)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
