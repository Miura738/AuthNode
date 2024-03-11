from fastapi import FastAPI
from fastapi.requests import Request

import yggdrasil

app = FastAPI(
    title="AuthNode"
)

# initialize FastAPI app
from config import init

init(app)


app.include_router(yggdrasil.app, prefix="/api", tags=["Yggdrasil API"])

