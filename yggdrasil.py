
from fastapi import APIRouter
from fastapi.requests import Request

app = APIRouter()

# Connect Database (MongoDB)
from mongo import db


# Authlib-Injector Verify API
@app.get("")
async def root(request: Request):
    # Get request host to add skin server list
    host = request.url.hostname

    # 获取公钥
    public_key = db("keys").find_one({"_id": "public_key"}, {"key": 1, "_id": 0})
    if public_key is None:
        # 没有生成过公钥， 检查私钥
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        private_key = db("keys").find_one({"_id": "private_key"}, {"key": 1, "_id": 0})
        # 没有生成过私钥，生成私钥
        if private_key is None:
            # 生成4096位RSA私钥
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=4096,
                backend=default_backend()
            )

            # 将私钥序列化为PEM格式
            private_key = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()  # 不使用密码加密私钥
            )

            db("keys").insert_one({"_id": "private_key", "key": private_key})
        else:
            private_key = private_key["key"]

        ## 生成公钥
        # 从序列化的私钥中加载私钥对象
        loaded_private_key = serialization.load_pem_private_key(
            private_key,
            password=None,
            backend=default_backend()
        )

        # 从私钥对象中获取公钥对象
        public_key = loaded_private_key.public_key()

        # 将公钥序列化为PEM格式
        public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        db("keys").insert_one({"_id": "public_key", "key": public_key})
    else:
        public_key = public_key["key"]

    return {
        "meta": {
            "implementationName": "AuthNode",
            "implementationVersion": "0.0.1",
            "serverName": "AoMiura's Minecraft Authentication Server",
            "feature.non_email_login": True
        },
        "skinDomains": [
            "*",
            ".minecraft.net",
            ".mojang.com",
            host
        ],
        "signaturePublickey": public_key.decode("utf-8")
    }

import authserver
import sessionserver
# Other API Router

app.include_router(sessionserver.router, prefix="/sessionserver", tags=["sessionserver"])
app.include_router(sessionserver.router, prefix="//sessionserver", tags=["sessionserver"])
app.include_router(authserver.router, prefix="/authserver", tags=["authserver"])
app.include_router(authserver.router, prefix="//authserver", tags=["authserver"])
