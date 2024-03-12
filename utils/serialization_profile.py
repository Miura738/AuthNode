import json
import time

from mongo import db
from utils.uuid_utils import uuid_parse

import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def serialize_profile(UserData, unsigned: bool = True):
    UserID = uuid_parse(str(UserData["_id"]))

    UserTextures = {
        "timestamp": int(time.time() * 1000),
        "profileId": UserID,
        "profileName": UserData["username"],
        "signatureRequired": False,
        "textures": UserData["textures"]
    }
    UserTextures = json.dumps(UserTextures, indent=2)
    UserTextures = base64.b64encode(str(UserTextures).encode("utf-8")).decode("utf-8")

    UserProfile = {
        "id": UserID,
        "name": UserData["username"],
        "properties": [{
            "name": "textures",
            "value": UserTextures
        }]
    }

    if not unsigned:
        private_key = db("keys").find_one({"_id": "private_key"}, {"key": 1, "_id": 0})
        private_key = (private_key["key"])
        private_key = serialization.load_pem_private_key(
            private_key,
            password=None,
            backend=default_backend()
        )
        signature = private_key.sign(
            UserTextures.encode(),
            padding.PKCS1v15(),
            hashes.SHA1()
        )
        signature_base64 = base64.b64encode(signature).decode('utf-8')

        UserProfile["properties"][0]["signature"] = signature_base64

    return UserProfile
